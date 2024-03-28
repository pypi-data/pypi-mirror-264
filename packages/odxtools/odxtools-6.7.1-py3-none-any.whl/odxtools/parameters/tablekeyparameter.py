# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from xml.etree import ElementTree

from typing_extensions import override

from ..decodestate import DecodeState
from ..encodestate import EncodeState
from ..exceptions import DecodeError, EncodeError, odxraise, odxrequire
from ..odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId, OdxLinkRef
from ..odxtypes import ParameterValue
from ..utils import dataclass_fields_asdict
from .parameter import Parameter, ParameterType

if TYPE_CHECKING:
    from ..diaglayer import DiagLayer
    from ..table import Table
    from ..tablerow import TableRow


@dataclass
class TableKeyParameter(Parameter):

    odx_id: OdxLinkId
    table_ref: Optional[OdxLinkRef]
    table_snref: Optional[str]
    table_row_snref: Optional[str]
    table_row_ref: Optional[OdxLinkRef]

    @staticmethod
    @override
    def from_et(et_element: ElementTree.Element,
                doc_frags: List[OdxDocFragment]) -> "TableKeyParameter":

        kwargs = dataclass_fields_asdict(Parameter.from_et(et_element, doc_frags))

        odx_id = odxrequire(OdxLinkId.from_et(et_element, doc_frags))

        table_ref = OdxLinkRef.from_et(et_element.find("TABLE-REF"), doc_frags)
        table_snref = None
        if (table_snref_elem := et_element.find("TABLE-SNREF")) is not None:
            table_snref = odxrequire(table_snref_elem.get("SHORT-NAME"))

        table_row_ref = OdxLinkRef.from_et(et_element.find("TABLE-ROW-REF"), doc_frags)
        table_row_snref = None
        if (table_row_snref_elem := et_element.find("TABLE-ROW-SNREF")) is not None:
            table_row_snref = odxrequire(table_row_snref_elem.get("SHORT-NAME"))

        return TableKeyParameter(
            odx_id=odx_id,
            table_ref=table_ref,
            table_snref=table_snref,
            table_row_ref=table_row_ref,
            table_row_snref=table_row_snref,
            **kwargs)

    def __post_init__(self) -> None:
        self._table: "Table"
        self._table_row: Optional["TableRow"] = None
        if self.table_ref is None and self.table_snref is None and \
           self.table_row_ref is None and self.table_row_snref is None:
            odxraise("Either a table or a table row must be defined.")

    @property
    @override
    def parameter_type(self) -> ParameterType:
        return "TABLE-KEY"

    @override
    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        result = super()._build_odxlinks()

        result[self.odx_id] = self

        return result

    @override
    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        super()._resolve_odxlinks(odxlinks)

        # Either table_ref or table_row_ref will be defined
        if self.table_ref:
            if TYPE_CHECKING:
                self._table = odxlinks.resolve(self.table_ref, Table)
            else:
                self._table = odxlinks.resolve(self.table_ref)

        if self.table_row_ref:
            if TYPE_CHECKING:
                self._table_row = odxlinks.resolve(self.table_row_ref, TableRow)
            else:
                self._table_row = odxlinks.resolve(self.table_row_ref)
            self._table = self._table_row.table

    @override
    def _resolve_snrefs(self, diag_layer: "DiagLayer") -> None:
        super()._resolve_snrefs(diag_layer)

        if self.table_snref is not None:
            ddd_spec = diag_layer.diag_data_dictionary_spec
            self._table = ddd_spec.tables[self.table_snref]
        if self.table_row_snref is not None:
            # make sure that we know the table to which the table row
            # SNREF is relative to.
            table = odxrequire(
                self._table, "If a table-row short name reference is defined, a "
                "table must also be specified.")
            self._table_row = table.table_rows[self.table_row_snref]

    @property
    def table(self) -> "Table":
        if self._table is not None:
            return self._table
        if self._table_row is not None:
            return self._table_row.table
        odxraise(f'Could not resolve the table of {self.short_name}')

    @property
    def table_row(self) -> Optional["TableRow"]:
        return self._table_row

    @property
    @override
    def is_required(self) -> bool:
        # TABLE-KEY parameters can be implicitly determined from the
        # corresponding TABLE-STRUCT
        return False

    @property
    @override
    def is_settable(self) -> bool:
        return True

    @override
    def get_coded_value_as_bytes(self, encode_state: EncodeState) -> bytes:
        tr_short_name = encode_state.parameter_values.get(self.short_name)

        if tr_short_name is None:
            # the table key has not been defined explicitly yet, but
            # it is most likely implicitly defined by the associated
            # TABLE-STRUCT parameters. Use all-zeros as a standin for
            # the real data...
            key_dop = self.table.key_dop
            if key_dop is None:
                raise EncodeError(f"Table '{self.table.short_name}' does not define "
                                  f"a KEY-DOP, but is used in TABLE-KEY parameter "
                                  f"'{self.short_name}'")

            byte_len = (odxrequire(key_dop.get_static_bit_length()) + 7) // 8
            if self.bit_position is not None and self.bit_position > 0:
                byte_len += 1

            return bytes([0] * byte_len)

        # the table key is known. We need to encode the associated DOP
        # into the PDU.
        tr_candidates = [x for x in self.table.table_rows if x.short_name == tr_short_name]
        if len(tr_candidates) == 0:
            raise EncodeError(f"No table row with short name '{tr_short_name}' found")
        elif len(tr_candidates) > 1:
            raise EncodeError(f"Multiple rows exhibiting short name '{tr_short_name}'")
        tr = tr_candidates[0]

        key_dop = self.table.key_dop
        if key_dop is None:
            raise EncodeError(f"Table '{self.table.short_name}' does not define "
                              f"a KEY-DOP, but is used in TABLE-KEY parameter "
                              f"'{self.short_name}'")
        bit_position = 0 if self.bit_position is None else self.bit_position
        return key_dop.convert_physical_to_bytes(tr.key, encode_state, bit_position=bit_position)

    @override
    def encode_into_pdu(self, encode_state: EncodeState) -> bytes:
        return super().encode_into_pdu(encode_state)

    @override
    def _decode_positioned_from_pdu(self, decode_state: DecodeState) -> ParameterValue:
        if self.table_row is not None:
            # the table row to be used is statically specified -> no
            # need to decode anything!
            phys_val = self.table_row.short_name
        else:
            # Use DOP to decode
            key_dop = odxrequire(self.table.key_dop)
            key_dop_val = key_dop.decode_from_pdu(decode_state)

            table_row_candidates = [x for x in self.table.table_rows if x.key == key_dop_val]
            if len(table_row_candidates) == 0:
                raise DecodeError(f"No table row exhibiting the key '{str(key_dop_val)}' found")
            elif len(table_row_candidates) > 1:
                raise DecodeError(
                    f"Multiple rows exhibiting key '{str(key_dop_val)}' found in table")
            table_row = table_row_candidates[0]
            phys_val = table_row.short_name

            # update the decode_state's table key
            decode_state.table_keys[self.short_name] = table_row

        return phys_val
