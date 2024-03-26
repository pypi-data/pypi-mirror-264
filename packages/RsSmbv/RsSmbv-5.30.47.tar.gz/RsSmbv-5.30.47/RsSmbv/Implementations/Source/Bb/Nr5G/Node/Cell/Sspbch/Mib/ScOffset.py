from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScOffsetCls:
	"""ScOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scOffset", core, parent)

	def set(self, ssp_bch_custom_ssb: float, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:SCOFfset \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.mib.scOffset.set(ssp_bch_custom_ssb = 1.0, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Queries the SS/PBCH subcarrier offset. \n
			:param ssp_bch_custom_ssb: float Range: 0 to 31
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.decimal_value_to_str(ssp_bch_custom_ssb)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:SCOFfset {param}')

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:SCOFfset \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.sspbch.mib.scOffset.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Queries the SS/PBCH subcarrier offset. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: ssp_bch_custom_ssb: float Range: 0 to 31"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:SCOFfset?')
		return Conversions.str_to_float(response)
