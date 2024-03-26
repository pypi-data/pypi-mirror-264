from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CellIdCls:
	"""CellId commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cellId", core, parent)

	def set(self, cell_id: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:CELLid \n
		Snippet: driver.source.bb.nr5G.node.cell.cellId.set(cell_id = 1, cellNull = repcap.CellNull.Default) \n
		Sets the cell identity of the selected cell. \n
			:param cell_id: integer For sidelink, the cell ID range isr 0 to 671. Range: 0 to 1007
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(cell_id)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:CELLid {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:CELLid \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.cellId.get(cellNull = repcap.CellNull.Default) \n
		Sets the cell identity of the selected cell. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: cell_id: integer For sidelink, the cell ID range isr 0 to 671. Range: 0 to 1007"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:CELLid?')
		return Conversions.str_to_int(response)
