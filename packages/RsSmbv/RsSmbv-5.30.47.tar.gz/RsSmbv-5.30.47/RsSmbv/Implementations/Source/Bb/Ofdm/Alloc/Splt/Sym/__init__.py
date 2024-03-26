from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymCls:
	"""Sym commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sym", core, parent)

	@property
	def size(self):
		"""size commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_size'):
			from .Size import SizeCls
			self._size = SizeCls(self._core, self._cmd_group)
		return self._size

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_step'):
			from .Step import StepCls
			self._step = StepCls(self._core, self._cmd_group)
		return self._step

	def clone(self) -> 'SymCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SymCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
