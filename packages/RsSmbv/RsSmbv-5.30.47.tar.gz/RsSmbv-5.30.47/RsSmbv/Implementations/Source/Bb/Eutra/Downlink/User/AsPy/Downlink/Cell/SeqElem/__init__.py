from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqElemCls:
	"""SeqElem commands group definition. 12 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seqElem", core, parent)

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def harq(self):
		"""harq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def pdre(self):
		"""pdre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdre'):
			from .Pdre import PdreCls
			self._pdre = PdreCls(self._core, self._cmd_group)
		return self._pdre

	@property
	def subframe(self):
		"""subframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subframe'):
			from .Subframe import SubframeCls
			self._subframe = SubframeCls(self._core, self._cmd_group)
		return self._subframe

	@property
	def tb1(self):
		"""tb1 commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb1'):
			from .Tb1 import Tb1Cls
			self._tb1 = Tb1Cls(self._core, self._cmd_group)
		return self._tb1

	@property
	def tb2(self):
		"""tb2 commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb2'):
			from .Tb2 import Tb2Cls
			self._tb2 = Tb2Cls(self._core, self._cmd_group)
		return self._tb2

	def clone(self) -> 'SeqElemCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SeqElemCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
