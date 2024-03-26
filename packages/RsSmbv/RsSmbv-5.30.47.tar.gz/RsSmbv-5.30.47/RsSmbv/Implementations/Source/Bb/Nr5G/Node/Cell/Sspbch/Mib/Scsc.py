from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScscCls:
	"""Scsc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scsc", core, parent)

	def set(self, ssp_bch_scs_common: enums.ScscOmmon, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:SCSC \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.mib.scsc.set(ssp_bch_scs_common = enums.ScscOmmon.N15_60, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects the common SCS (subcarrier spacing) . \n
			:param ssp_bch_scs_common: N15_60| N30_120
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(ssp_bch_scs_common, enums.ScscOmmon)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:SCSC {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> enums.ScscOmmon:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:SCSC \n
		Snippet: value: enums.ScscOmmon = driver.source.bb.nr5G.node.cell.sspbch.mib.scsc.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects the common SCS (subcarrier spacing) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: ssp_bch_scs_common: N15_60| N30_120"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:SCSC?')
		return Conversions.str_to_scalar_enum(response, enums.ScscOmmon)
