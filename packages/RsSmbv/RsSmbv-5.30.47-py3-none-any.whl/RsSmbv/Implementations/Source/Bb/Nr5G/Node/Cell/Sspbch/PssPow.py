from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PssPowCls:
	"""PssPow commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pssPow", core, parent)

	def set(self, pss_power: float, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:PSSPow \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.pssPow.set(pss_power = 1.0, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Sets the power of the SSS/PSS/PBCH allocations relative to the power of the other resource elements. For the sidelink
		application: power of S-PSS, S-SSS and PSBCH. \n
			:param pss_power: float Range: -80.0 to 10.0
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.decimal_value_to_str(pss_power)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:PSSPow {param}')

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:PSSPow \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.sspbch.pssPow.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Sets the power of the SSS/PSS/PBCH allocations relative to the power of the other resource elements. For the sidelink
		application: power of S-PSS, S-SSS and PSBCH. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: pss_power: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:PSSPow?')
		return Conversions.str_to_float(response)
