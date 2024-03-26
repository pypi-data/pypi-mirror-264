from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TaposCls:
	"""Tapos commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tapos", core, parent)

	def set(self, dmrs_type_apos: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TAPos \n
		Snippet: driver.source.bb.nr5G.node.cell.tapos.set(dmrs_type_apos = 1, cellNull = repcap.CellNull.Default) \n
		Sets the position of the first DMRS symbol within the slot, if mapping type A is used. \n
			:param dmrs_type_apos: integer Range: 2 to 3
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(dmrs_type_apos)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TAPos {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TAPos \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.tapos.get(cellNull = repcap.CellNull.Default) \n
		Sets the position of the first DMRS symbol within the slot, if mapping type A is used. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: dmrs_type_apos: integer Range: 2 to 3"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TAPos?')
		return Conversions.str_to_int(response)
