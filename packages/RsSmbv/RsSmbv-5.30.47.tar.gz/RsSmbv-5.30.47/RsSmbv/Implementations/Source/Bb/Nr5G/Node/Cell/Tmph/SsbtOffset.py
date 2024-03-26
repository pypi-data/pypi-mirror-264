from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SsbtOffsetCls:
	"""SsbtOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ssbtOffset", core, parent)

	def set(self, ssb_time_offset: enums.TimeOffset, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TMPH:SSBToffset \n
		Snippet: driver.source.bb.nr5G.node.cell.tmph.ssbtOffset.set(ssb_time_offset = enums.TimeOffset.S0, cellNull = repcap.CellNull.Default) \n
		Defines a time offset for the SS/PBCH block. \n
			:param ssb_time_offset: S0| S5| S10| S15 Time offset in milliseconds (0, 5, 10 and 15 ms) .
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.enum_scalar_to_str(ssb_time_offset, enums.TimeOffset)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TMPH:SSBToffset {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.TimeOffset:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TMPH:SSBToffset \n
		Snippet: value: enums.TimeOffset = driver.source.bb.nr5G.node.cell.tmph.ssbtOffset.get(cellNull = repcap.CellNull.Default) \n
		Defines a time offset for the SS/PBCH block. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: ssb_time_offset: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TMPH:SSBToffset?')
		return Conversions.str_to_scalar_enum(response, enums.TimeOffset)
