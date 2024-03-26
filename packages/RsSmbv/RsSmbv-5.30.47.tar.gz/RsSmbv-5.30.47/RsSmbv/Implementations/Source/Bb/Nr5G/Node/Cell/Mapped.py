from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MappedCls:
	"""Mapped commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mapped", core, parent)

	def set(self, cell_mapped: bool, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:MAPPed \n
		Snippet: driver.source.bb.nr5G.node.cell.mapped.set(cell_mapped = False, cellNull = repcap.CellNull.Default) \n
		If enabled, the signal of the selected cell is mapped to the output. \n
			:param cell_mapped: 1| ON| 0| OFF
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.bool_to_str(cell_mapped)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:MAPPed {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:MAPPed \n
		Snippet: value: bool = driver.source.bb.nr5G.node.cell.mapped.get(cellNull = repcap.CellNull.Default) \n
		If enabled, the signal of the selected cell is mapped to the output. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: cell_mapped: 1| ON| 0| OFF"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:MAPPed?')
		return Conversions.str_to_bool(response)
