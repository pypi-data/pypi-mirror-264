from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StatisticsCls:
	"""Statistics commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("statistics", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Cmd_Hw_Time: List[float]: float The hardware time at the moment the last HIL command is received.
			- Last_Latency: float: float Time delay between the time specified with the parameter ElapsedTime in a HIL command and the time this command is executed in the R&S SMBV100B. Unit: s
			- Max_Latency: float: float The largest latency value since the last time this query was sent. Unit: s
			- Min_Latency: float: float The smallest latency value since the last time this query was sent. Unit: s
			- No_Zero_Values: int: integer Number of non-zero latency values since the last time this query was sent.
			- Cmd_Received: int: integer Accumulated LastLatency values since the last time this query was sent.
			- Cmd_Used: int: integer The number of used HIL commands, excluding the dropped HIL commands, since the last time this query was sent.
			- Cmd_Sync: int: integer The number of HIL commands applied at their specified time
			- Cmd_Exterp: int: integer The number of extrapolated HIL commands. The commands are applied later than their specified time.
			- Cmd_Interp: int: integer The number of internal position updates. The value includes commands describing both situations, moment of time in past and moment of time in the future.
			- Cmd_Predict: int: integer The number of internal position updates performed by the prediction algorithm, see 'Trajectory prediction'.
			- Max_Used: int: integer The maximum number buffered commands
			- Min_Used: int: integer The minimum number buffered commands"""
		__meta_args_list = [
			ArgStruct('Cmd_Hw_Time', DataType.FloatList, None, False, True, 1),
			ArgStruct.scalar_float('Last_Latency'),
			ArgStruct.scalar_float('Max_Latency'),
			ArgStruct.scalar_float('Min_Latency'),
			ArgStruct.scalar_int('No_Zero_Values'),
			ArgStruct.scalar_int('Cmd_Received'),
			ArgStruct.scalar_int('Cmd_Used'),
			ArgStruct.scalar_int('Cmd_Sync'),
			ArgStruct.scalar_int('Cmd_Exterp'),
			ArgStruct.scalar_int('Cmd_Interp'),
			ArgStruct.scalar_int('Cmd_Predict'),
			ArgStruct.scalar_int('Max_Used'),
			ArgStruct.scalar_int('Min_Used')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cmd_Hw_Time: List[float] = None
			self.Last_Latency: float = None
			self.Max_Latency: float = None
			self.Min_Latency: float = None
			self.No_Zero_Values: int = None
			self.Cmd_Received: int = None
			self.Cmd_Used: int = None
			self.Cmd_Sync: int = None
			self.Cmd_Exterp: int = None
			self.Cmd_Interp: int = None
			self.Cmd_Predict: int = None
			self.Max_Used: int = None
			self.Min_Used: int = None

	def get(self, vehicle=repcap.Vehicle.Default) -> GetStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RT:RECeiver:[V<ST>]:HILPosition:LATency:STATistics \n
		Snippet: value: GetStruct = driver.source.bb.gnss.rt.receiver.v.hilPosition.latency.statistics.get(vehicle = repcap.Vehicle.Default) \n
		Queries the current latency tcal.latency,i and statistics on the latency values. This command returns also the minimum
		deviation and the maximum deviation from zero latency. Also, it returns the measured number of non-zero latency values
		since the last query with this command.
			INTRO_CMD_HELP: The following terms are used: \n
			- HIL command refers to HiL mode A or HiL mode B commands: [:SOURce<hw>]:BB:GNSS:RT:RECeiver[:V<st>]:HILPosition:MODE:A [:SOURce<hw>]:BB:GNSS:RT:RECeiver[:V<st>]:HILPosition:MODE:B
			- Dropped commands are commands that are evaluated, buffered but not applied because they become outdated as more up-to-date information is received
			- Return values apply for the period since the last query with this command.
		How to: 'Latency calibration' \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:RT:RECeiver:V{vehicle_cmd_val}:HILPosition:LATency:STATistics?', self.__class__.GetStruct())
