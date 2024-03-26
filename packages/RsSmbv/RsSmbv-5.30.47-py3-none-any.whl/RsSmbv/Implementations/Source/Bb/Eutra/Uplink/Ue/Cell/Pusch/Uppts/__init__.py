from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UpptsCls:
	"""Uppts commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uppts", core, parent)

	@property
	def ldMrs(self):
		"""ldMrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ldMrs'):
			from .LdMrs import LdMrsCls
			self._ldMrs = LdMrsCls(self._core, self._cmd_group)
		return self._ldMrs

	@property
	def nsym(self):
		"""nsym commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsym'):
			from .Nsym import NsymCls
			self._nsym = NsymCls(self._core, self._cmd_group)
		return self._nsym

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'UpptsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UpptsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
