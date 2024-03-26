from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	def set(self, hour: int, minute: int, second: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:MCCW:TRIGger:TIME:TIME \n
		Snippet: driver.source.bb.mccw.trigger.time.time.set(hour = 1, minute = 1, second = 1) \n
		Sets the time for a time-based trigger signal. For trigger modes single or armed auto, you can activate triggering at
		this time via the following command: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:STATe <DigStd> is the mnemonic for the digital
		standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support this feature. \n
			:param hour: integer Range: 0 to 23
			:param minute: integer Range: 0 to 59
			:param second: integer Range: 0 to 59
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('hour', hour, DataType.Integer), ArgSingle('minute', minute, DataType.Integer), ArgSingle('second', second, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:TRIGger:TIME:TIME {param}'.rstrip())

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):
		"""Response structure. Fields: \n
			- Hour: int: integer Range: 0 to 23
			- Minute: int: integer Range: 0 to 59
			- Second: int: integer Range: 0 to 59"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_int('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: int = None

	def get(self) -> TimeStruct:
		"""SCPI: [SOURce<HW>]:BB:MCCW:TRIGger:TIME:TIME \n
		Snippet: value: TimeStruct = driver.source.bb.mccw.trigger.time.time.get() \n
		Sets the time for a time-based trigger signal. For trigger modes single or armed auto, you can activate triggering at
		this time via the following command: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:STATe <DigStd> is the mnemonic for the digital
		standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support this feature. \n
			:return: structure: for return value, see the help for TimeStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:MCCW:TRIGger:TIME:TIME?', self.__class__.TimeStruct())
