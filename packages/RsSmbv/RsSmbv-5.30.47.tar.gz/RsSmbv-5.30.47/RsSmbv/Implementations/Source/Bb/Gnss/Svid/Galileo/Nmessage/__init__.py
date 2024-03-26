from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NmessageCls:
	"""Nmessage commands group definition. 93 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nmessage", core, parent)

	@property
	def fnav(self):
		"""fnav commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fnav'):
			from .Fnav import FnavCls
			self._fnav = FnavCls(self._core, self._cmd_group)
		return self._fnav

	@property
	def inav(self):
		"""inav commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_inav'):
			from .Inav import InavCls
			self._inav = InavCls(self._core, self._cmd_group)
		return self._inav

	def clone(self) -> 'NmessageCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NmessageCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
