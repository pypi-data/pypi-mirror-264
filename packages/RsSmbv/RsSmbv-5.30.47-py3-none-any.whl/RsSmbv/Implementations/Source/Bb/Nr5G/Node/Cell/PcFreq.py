from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PcFreqCls:
	"""PcFreq commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pcFreq", core, parent)

	def set(self, carrier_freq: float, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:PCFReq \n
		Snippet: driver.source.bb.nr5G.node.cell.pcFreq.set(carrier_freq = 1.0, cellNull = repcap.CellNull.Default) \n
		Sets the carrier frequency of the selected carrier at which the frequency phase compensation is applied. \n
			:param carrier_freq: float Range: 0 to 999E9
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(carrier_freq)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:PCFReq {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:PCFReq \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.pcFreq.get(cellNull = repcap.CellNull.Default) \n
		Sets the carrier frequency of the selected carrier at which the frequency phase compensation is applied. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: carrier_freq: float Range: 0 to 999E9"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:PCFReq?')
		return Conversions.str_to_float(response)
