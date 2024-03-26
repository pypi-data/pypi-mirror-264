from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PcqiCls:
	"""Pcqi commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pcqi", core, parent)

	@property
	def repeat(self):
		"""repeat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repeat'):
			from .Repeat import RepeatCls
			self._repeat = RepeatCls(self._core, self._cmd_group)
		return self._repeat

	@property
	def rows(self):
		"""rows commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rows'):
			from .Rows import RowsCls
			self._rows = RowsCls(self._core, self._cmd_group)
		return self._rows

	def clone(self) -> 'PcqiCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PcqiCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
