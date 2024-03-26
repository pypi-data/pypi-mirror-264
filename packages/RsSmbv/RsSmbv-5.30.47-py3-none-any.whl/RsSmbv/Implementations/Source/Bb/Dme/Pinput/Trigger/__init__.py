from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	def get_search(self) -> bool:
		"""SCPI: [SOURce<HW>]:[BB]:DME:PINPut:TRIGger:SEARch \n
		Snippet: value: bool = driver.source.bb.dme.pinput.trigger.get_search() \n
		Determines the trigger level that is the 50% voltage point of first pulse of the external DME interrogation signal.
		Determination of the trigger point requires a connected power sensor. Use a power sensor, for example the R&S NRP-Z81, to
		receive the external DME signal. Repeat the trigger search function when changing the level of the external DME signal. \n
			:return: search: 1| ON| 0| OFF 1|ON No trigger level found 0|OFF Trigger level found
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PINPut:TRIGger:SEARch?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
