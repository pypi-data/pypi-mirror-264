from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	@property
	def destination(self):
		"""destination commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_destination'):
			from .Destination import DestinationCls
			self._destination = DestinationCls(self._core, self._cmd_group)
		return self._destination

	@property
	def fselect(self):
		"""fselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fselect'):
			from .Fselect import FselectCls
			self._fselect = FselectCls(self._core, self._cmd_group)
		return self._fselect

	def clone(self) -> 'OutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
