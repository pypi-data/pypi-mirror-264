from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class S960KCls:
	"""S960K commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("s960K", core, parent)

	@property
	def use(self):
		"""use commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_use'):
			from .Use import UseCls
			self._use = UseCls(self._core, self._cmd_group)
		return self._use

	def clone(self) -> 'S960KCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = S960KCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
