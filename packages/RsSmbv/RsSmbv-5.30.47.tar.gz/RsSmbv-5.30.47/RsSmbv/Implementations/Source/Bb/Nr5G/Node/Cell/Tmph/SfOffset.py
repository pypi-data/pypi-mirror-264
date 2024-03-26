from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfOffsetCls:
	"""SfOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sfOffset", core, parent)

	def set(self, sub_frame_offset: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TMPH:SFOFfset \n
		Snippet: driver.source.bb.nr5G.node.cell.tmph.sfOffset.set(sub_frame_offset = 1, cellNull = repcap.CellNull.Default) \n
		Defines a cell specific cyclic subframe shift in terms of subframes. \n
			:param sub_frame_offset: integer Range: 0 to 10
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(sub_frame_offset)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TMPH:SFOFfset {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TMPH:SFOFfset \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.tmph.sfOffset.get(cellNull = repcap.CellNull.Default) \n
		Defines a cell specific cyclic subframe shift in terms of subframes. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: sub_frame_offset: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TMPH:SFOFfset?')
		return Conversions.str_to_int(response)
