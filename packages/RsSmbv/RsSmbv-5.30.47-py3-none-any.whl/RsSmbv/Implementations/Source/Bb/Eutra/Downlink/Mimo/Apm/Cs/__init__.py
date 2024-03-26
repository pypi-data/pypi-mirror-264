from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsCls:
	"""Cs commands group definition. 3 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cs", core, parent)

	@property
	def ap(self):
		"""ap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap'):
			from .Ap import ApCls
			self._ap = ApCls(self._core, self._cmd_group)
		return self._ap

	@property
	def cell(self):
		"""cell commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	def clone(self) -> 'CsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
