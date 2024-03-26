from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MoneCls:
	"""Mone commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mone", core, parent)

	@property
	def tipo(self):
		"""tipo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tipo'):
			from .Tipo import TipoCls
			self._tipo = TipoCls(self._core, self._cmd_group)
		return self._tipo

	def clone(self) -> 'MoneCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MoneCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
