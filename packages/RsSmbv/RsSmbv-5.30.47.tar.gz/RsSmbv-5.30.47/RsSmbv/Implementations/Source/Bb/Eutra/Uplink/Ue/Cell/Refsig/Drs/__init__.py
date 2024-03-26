from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DrsCls:
	"""Drs commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("drs", core, parent)

	@property
	def dwocc(self):
		"""dwocc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dwocc'):
			from .Dwocc import DwoccCls
			self._dwocc = DwoccCls(self._core, self._cmd_group)
		return self._dwocc

	@property
	def enhanced(self):
		"""enhanced commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enhanced'):
			from .Enhanced import EnhancedCls
			self._enhanced = EnhancedCls(self._core, self._cmd_group)
		return self._enhanced

	@property
	def powOffset(self):
		"""powOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_powOffset'):
			from .PowOffset import PowOffsetCls
			self._powOffset = PowOffsetCls(self._core, self._cmd_group)
		return self._powOffset

	def clone(self) -> 'DrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
