from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScCls:
	"""Sc commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sc", core, parent)

	@property
	def active(self):
		"""active commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_active'):
			from .Active import ActiveCls
			self._active = ActiveCls(self._core, self._cmd_group)
		return self._active

	@property
	def enabled(self):
		"""enabled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enabled'):
			from .Enabled import EnabledCls
			self._enabled = EnabledCls(self._core, self._cmd_group)
		return self._enabled

	def clone(self) -> 'ScCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
