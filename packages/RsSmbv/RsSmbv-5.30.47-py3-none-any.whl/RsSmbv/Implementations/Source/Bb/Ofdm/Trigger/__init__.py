from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 23 total commands, 6 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	@property
	def arm(self):
		"""arm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arm'):
			from .Arm import ArmCls
			self._arm = ArmCls(self._core, self._cmd_group)
		return self._arm

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	@property
	def external(self):
		"""external commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	@property
	def output(self):
		"""output commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:RMODe \n
		Snippet: value: enums.TrigRunMode = driver.source.bb.ofdm.trigger.get_rmode() \n
		Queries the status of waveform output. \n
			:return: trig_run_mode: STOP| RUN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:TRIGger:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:SLENgth \n
		Snippet: value: int = driver.source.bb.ofdm.trigger.get_slength() \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:return: trig_seq_len: integer Range: 1 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:TRIGger:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, trig_seq_len: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:SLENgth \n
		Snippet: driver.source.bb.ofdm.trigger.set_slength(trig_seq_len = 1) \n
		Defines the length of the signal sequence to be output in the SINGle trigger mode. \n
			:param trig_seq_len: integer Range: 1 to dynamic
		"""
		param = Conversions.decimal_value_to_str(trig_seq_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:TRIGger:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_sl_unit(self) -> enums.UnitSlB:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:SLUNit \n
		Snippet: value: enums.UnitSlB = driver.source.bb.ofdm.trigger.get_sl_unit() \n
		Defines the unit for the entry of the length of the signal sequence to be output in the SINGle trigger mode. \n
			:return: trig_seq_len_unit: SEQuence| SAMPle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:TRIGger:SLUNit?')
		return Conversions.str_to_scalar_enum(response, enums.UnitSlB)

	def set_sl_unit(self, trig_seq_len_unit: enums.UnitSlB) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:SLUNit \n
		Snippet: driver.source.bb.ofdm.trigger.set_sl_unit(trig_seq_len_unit = enums.UnitSlB.SAMPle) \n
		Defines the unit for the entry of the length of the signal sequence to be output in the SINGle trigger mode. \n
			:param trig_seq_len_unit: SEQuence| SAMPle
		"""
		param = Conversions.enum_scalar_to_str(trig_seq_len_unit, enums.UnitSlB)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:TRIGger:SLUNit {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TrigSour:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:SOURce \n
		Snippet: value: enums.TrigSour = driver.source.bb.ofdm.trigger.get_source() \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors EGT1: External global trigger
			- In primary-secondary instrument mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde & Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:return: trig_source: INTernal| EGT1| EXTernal| BBSY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSour)

	def set_source(self, trig_source: enums.TrigSour) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:TRIGger:SOURce \n
		Snippet: driver.source.bb.ofdm.trigger.set_source(trig_source = enums.TrigSour.BBSY) \n
			INTRO_CMD_HELP: Selects the trigger signal source and determines the way the triggering is executed. Provided are: \n
			- Internal triggering by a command (INTernal)
			- External trigger signal via one of the User x connectors EGT1: External global trigger
			- In primary-secondary instrument mode, the external baseband synchronization signal (BBSY)
			- EXTernal: Setting only Provided only for backward compatibility with other Rohde & Schwarz signal generators. The R&S SMBV100B accepts this value and maps it automatically as follows: EXTernal = EGT1 \n
			:param trig_source: INTernal| EGT1| EXTernal| BBSY
		"""
		param = Conversions.enum_scalar_to_str(trig_source, enums.TrigSour)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get_sequence(self) -> enums.DmTrigMode:
		"""SCPI: [SOURce<HW>]:BB:OFDM:[TRIGger]:SEQuence \n
		Snippet: value: enums.DmTrigMode = driver.source.bb.ofdm.trigger.get_sequence() \n
		Sets the trigger mode. \n
			:return: trig_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, trig_mode: enums.DmTrigMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:[TRIGger]:SEQuence \n
		Snippet: driver.source.bb.ofdm.trigger.set_sequence(trig_mode = enums.DmTrigMode.AAUTo) \n
		Sets the trigger mode. \n
			:param trig_mode: AUTO| RETRigger| AAUTo| ARETrigger| SINGle
		"""
		param = Conversions.enum_scalar_to_str(trig_mode, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:TRIGger:SEQuence {param}')

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
