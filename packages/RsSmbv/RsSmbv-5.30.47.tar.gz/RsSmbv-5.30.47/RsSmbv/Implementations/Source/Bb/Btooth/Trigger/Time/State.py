from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, hour: int, minute: int, second: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:TIME:[STATe] \n
		Snippet: driver.source.bb.btooth.trigger.time.state.set(hour = 1, minute = 1, second = 1) \n
		Activates time-based triggering with a fixed time reference. If activated, the R&S SMBV100B triggers signal generation
		when its operating system time matches a specified time. Specify the trigger date and trigger time with the following
		commands: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:DATE SOURce<hw>:BB:<DigStd>:TRIGger:TIME:TIME <DigStd> is the mnemonic for
		the digital standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support
		this feature. \n
			:param hour: integer Range: 0 to 23
			:param minute: integer Range: 0 to 59
			:param second: integer Range: 0 to 59
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('hour', hour, DataType.Integer), ArgSingle('minute', minute, DataType.Integer), ArgSingle('second', second, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:TIME:STATe {param}'.rstrip())

	# noinspection PyTypeChecker
	class StateStruct(StructBase):
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

	def get(self) -> StateStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:TIME:[STATe] \n
		Snippet: value: StateStruct = driver.source.bb.btooth.trigger.time.state.get() \n
		Activates time-based triggering with a fixed time reference. If activated, the R&S SMBV100B triggers signal generation
		when its operating system time matches a specified time. Specify the trigger date and trigger time with the following
		commands: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:DATE SOURce<hw>:BB:<DigStd>:TRIGger:TIME:TIME <DigStd> is the mnemonic for
		the digital standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support
		this feature. \n
			:return: structure: for return value, see the help for StateStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:TIME:STATe?', self.__class__.StateStruct())
