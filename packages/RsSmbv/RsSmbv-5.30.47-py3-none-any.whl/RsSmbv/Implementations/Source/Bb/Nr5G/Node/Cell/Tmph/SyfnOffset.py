from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyfnOffsetCls:
	"""SyfnOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("syfnOffset", core, parent)

	def set(self, sys_frm_num_off: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TMPH:SYFNoffset \n
		Snippet: driver.source.bb.nr5G.node.cell.tmph.syfnOffset.set(sys_frm_num_off = 1, cellNull = repcap.CellNull.Default) \n
		Sets an offset value for the system frame number. The first generated frame starts with the given system frame number
		offset. \n
			:param sys_frm_num_off: integer Range: 0 to 1023
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(sys_frm_num_off)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TMPH:SYFNoffset {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TMPH:SYFNoffset \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.tmph.syfnOffset.get(cellNull = repcap.CellNull.Default) \n
		Sets an offset value for the system frame number. The first generated frame starts with the given system frame number
		offset. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: sys_frm_num_off: integer Range: 0 to 1023"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TMPH:SYFNoffset?')
		return Conversions.str_to_int(response)
