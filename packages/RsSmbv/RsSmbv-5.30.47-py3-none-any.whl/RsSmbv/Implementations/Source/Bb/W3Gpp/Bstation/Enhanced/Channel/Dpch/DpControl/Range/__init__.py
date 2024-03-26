from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RangeCls:
	"""Range commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("range", core, parent)

	@property
	def down(self):
		"""down commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_down'):
			from .Down import DownCls
			self._down = DownCls(self._core, self._cmd_group)
		return self._down

	@property
	def up(self):
		"""up commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_up'):
			from .Up import UpCls
			self._up = UpCls(self._core, self._cmd_group)
		return self._up

	def clone(self) -> 'RangeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RangeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
