# SPDX-License-Identifier: MIT
import abc
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Union, cast

from .decodestate import ODX_TYPE_TO_FORMAT_LETTER, DecodeState
from .encodestate import EncodeState
from .exceptions import EncodeError, odxassert, odxraise
from .odxlink import OdxLinkDatabase, OdxLinkId
from .odxtypes import AtomicOdxType, DataType

try:
    import bitstruct.c as bitstruct
except ImportError:
    import bitstruct

if TYPE_CHECKING:
    from .diaglayer import DiagLayer

# Allowed diag-coded types
DctType = Literal[
    "LEADING-LENGTH-INFO-TYPE",
    "MIN-MAX-LENGTH-TYPE",
    "PARAM-LENGTH-INFO-TYPE",
    "STANDARD-LENGTH-TYPE",
]


@dataclass
class DiagCodedType(abc.ABC):

    base_data_type: DataType
    base_type_encoding: Optional[str]
    is_highlow_byte_order_raw: Optional[bool]

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:  # noqa: B027
        return {}

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:  # noqa: B027
        """Recursively resolve any odxlinks references"""
        pass

    def _resolve_snrefs(self, diag_layer: "DiagLayer") -> None:  # noqa: B027
        """Recursively resolve any short-name references"""
        pass

    def get_static_bit_length(self) -> Optional[int]:
        return None

    @property
    @abc.abstractmethod
    def dct_type(self) -> DctType:
        pass

    @property
    def is_highlow_byte_order(self) -> bool:
        return self.is_highlow_byte_order_raw in [None, True]

    @staticmethod
    def _encode_internal_value(
        internal_value: AtomicOdxType,
        bit_position: int,
        bit_length: int,
        base_data_type: DataType,
        is_highlow_byte_order: bool,
    ) -> bytes:
        """Convert the internal_value to bytes."""
        # Check that bytes and strings actually fit into the bit length
        if base_data_type == DataType.A_BYTEFIELD:
            if isinstance(internal_value, bytearray):
                internal_value = bytes(internal_value)
            if not isinstance(internal_value, bytes):
                odxraise()
            if 8 * len(internal_value) > bit_length:
                raise EncodeError(f"The bytefield {internal_value.hex()} is too large "
                                  f"({len(internal_value)} bytes)."
                                  f" The maximum length is {bit_length//8}.")
        if base_data_type == DataType.A_ASCIISTRING:
            if not isinstance(internal_value, str):
                odxraise()

            # The spec says ASCII, meaning only byte values 0-127.
            # But in practice, vendors use iso-8859-1, aka latin-1
            # reason being iso-8859-1 never fails since it has a valid
            # character mapping for every possible byte sequence.
            internal_value = internal_value.encode("iso-8859-1")

            if 8 * len(internal_value) > bit_length:
                raise EncodeError(f"The string {repr(internal_value)} is too large."
                                  f" The maximum number of characters is {bit_length//8}.")
        elif base_data_type == DataType.A_UTF8STRING:
            if not isinstance(internal_value, str):
                odxraise()

            internal_value = internal_value.encode("utf-8")

            if 8 * len(internal_value) > bit_length:
                raise EncodeError(f"The string {repr(internal_value)} is too large."
                                  f" The maximum number of bytes is {bit_length//8}.")

        elif base_data_type == DataType.A_UNICODE2STRING:
            if not isinstance(internal_value, str):
                odxraise()

            text_encoding = "utf-16-be" if is_highlow_byte_order else "utf-16-le"
            internal_value = internal_value.encode(text_encoding)

            if 8 * len(internal_value) > bit_length:
                raise EncodeError(f"The string {repr(internal_value)} is too large."
                                  f" The maximum number of characters is {bit_length//16}.")

        # If the bit length is zero, return empty bytes
        if bit_length == 0:
            if (base_data_type.value in [
                    DataType.A_INT32, DataType.A_UINT32, DataType.A_FLOAT32, DataType.A_FLOAT64
            ] and base_data_type.value != 0):
                raise EncodeError(
                    f"The number {repr(internal_value)} cannot be encoded into {bit_length} bits.")
            return b''

        char = ODX_TYPE_TO_FORMAT_LETTER[base_data_type]
        padding = (8 - ((bit_length + bit_position) % 8)) % 8
        odxassert((0 <= padding and padding < 8 and (padding + bit_length + bit_position) % 8 == 0),
                  f"Incorrect padding {padding}")
        left_pad = f"p{padding}" if padding > 0 else ""

        # actually encode the value
        coded = bitstruct.pack(f"{left_pad}{char}{bit_length}", internal_value)

        # apply byte order for numeric objects
        if not is_highlow_byte_order and base_data_type in [
                DataType.A_INT32,
                DataType.A_UINT32,
                DataType.A_FLOAT32,
                DataType.A_FLOAT64,
        ]:
            coded = coded[::-1]

        return cast(bytes, coded)

    def _minimal_byte_length_of(self, internal_value: Union[bytes, str]) -> int:
        """Helper method to get the minimal byte length.
        (needed for LeadingLength- and MinMaxLengthType)
        """
        byte_length: int = -1
        # A_BYTEFIELD, A_ASCIISTRING, A_UNICODE2STRING, A_UTF8STRING
        if self.base_data_type == DataType.A_BYTEFIELD:
            byte_length = len(internal_value)
        elif self.base_data_type in [DataType.A_ASCIISTRING, DataType.A_UTF8STRING]:
            if not isinstance(internal_value, str):
                odxraise()

            # TODO: Handle different encodings
            byte_length = len(bytes(internal_value, "utf-8"))
        elif self.base_data_type == DataType.A_UNICODE2STRING:
            if not isinstance(internal_value, str):
                odxraise()

            byte_length = len(bytes(internal_value, "utf-16-le"))
            odxassert(
                byte_length % 2 == 0, f"The bit length of A_UNICODE2STRING must"
                f" be a multiple of 16 but is {8*byte_length}")
        return byte_length

    @abc.abstractmethod
    def convert_internal_to_bytes(self, internal_value: AtomicOdxType, encode_state: EncodeState,
                                  bit_position: int) -> bytes:
        """Encode the internal value.

        Parameters
        ----------
        internal_value : python type corresponding to self.base_data_type
            the value to be encoded
        bit_position : int

        length_keys : Dict[OdxLinkId, int]
            mapping from ID (of the length key) to bit length
            (only needed for ParamLengthInfoType)
        """
        pass

    @abc.abstractmethod
    def decode_from_pdu(self, decode_state: DecodeState) -> AtomicOdxType:
        """Decode the parameter value from the coded message.

        Parameters
        ----------
        decode_state : DecodeState
            The decoding state

        Returns
        -------
        str or int or bytes or dict
            the decoded parameter value
        int
            the next byte position after the extracted parameter
        """
        pass
