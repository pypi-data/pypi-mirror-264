from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DownCls:
	"""Down commands group definition. 7 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("down", core, parent)

	@property
	def mc(self):
		"""mc commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_mc'):
			from .Mc import McCls
			self._mc = McCls(self._core, self._cmd_group)
		return self._mc

	def clone(self) -> 'DownCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DownCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
