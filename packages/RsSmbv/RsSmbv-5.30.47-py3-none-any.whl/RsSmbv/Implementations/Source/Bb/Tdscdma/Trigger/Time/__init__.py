from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .Date import DateCls
			self._date = DateCls(self._core, self._cmd_group)
		return self._date

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:TRIGger:TIME:[STATe] \n
		Snippet: value: bool = driver.source.bb.tdscdma.trigger.time.get_state() \n
		Activates time-based triggering with a fixed time reference. If activated, the R&S SMBV100B triggers signal generation
		when its operating system time matches a specified time. Specify the trigger date and trigger time with the following
		commands: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:DATE SOURce<hw>:BB:<DigStd>:TRIGger:TIME:TIME <DigStd> is the mnemonic for
		the digital standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support
		this feature. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:TRIGger:TIME:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:TRIGger:TIME:[STATe] \n
		Snippet: driver.source.bb.tdscdma.trigger.time.set_state(state = False) \n
		Activates time-based triggering with a fixed time reference. If activated, the R&S SMBV100B triggers signal generation
		when its operating system time matches a specified time. Specify the trigger date and trigger time with the following
		commands: SOURce<hw>:BB:<DigStd>:TRIGger:TIME:DATE SOURce<hw>:BB:<DigStd>:TRIGger:TIME:TIME <DigStd> is the mnemonic for
		the digital standard, for example, ARB. Time-based triggering behaves analogously for all digital standards that support
		this feature. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:TRIGger:TIME:STATe {param}')

	def clone(self) -> 'TimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
