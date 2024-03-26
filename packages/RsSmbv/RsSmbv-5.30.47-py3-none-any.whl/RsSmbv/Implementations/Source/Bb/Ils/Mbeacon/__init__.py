from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MbeaconCls:
	"""Mbeacon commands group definition. 16 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mbeacon", core, parent)

	@property
	def comid(self):
		"""comid commands group. 1 Sub-classes, 9 commands."""
		if not hasattr(self, '_comid'):
			from .Comid import ComidCls
			self._comid = ComidCls(self._core, self._cmd_group)
		return self._comid

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	def clone(self) -> 'MbeaconCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MbeaconCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
