from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: List[str], bitcount: int, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:PATTern \n
		Snippet: driver.source.bb.btooth.cs.sevent.pattern.set(pattern = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param pattern: No help available
			:param bitcount: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('pattern', pattern, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- Pattern: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def get(self, channelNull=repcap.ChannelNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.btooth.cs.sevent.pattern.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:PATTern?', self.__class__.PatternStruct())
