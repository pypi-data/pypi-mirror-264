from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqElemCls:
	"""SeqElem commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

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
	def ndi(self):
		"""ndi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndi'):
			from .Ndi import NdiCls
			self._ndi = NdiCls(self._core, self._cmd_group)
		return self._ndi

	@property
	def ptpc(self):
		"""ptpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptpc'):
			from .Ptpc import PtpcCls
			self._ptpc = PtpcCls(self._core, self._cmd_group)
		return self._ptpc

	@property
	def rba(self):
		"""rba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rba'):
			from .Rba import RbaCls
			self._rba = RbaCls(self._core, self._cmd_group)
		return self._rba

	@property
	def rv(self):
		"""rv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rv'):
			from .Rv import RvCls
			self._rv = RvCls(self._core, self._cmd_group)
		return self._rv

	@property
	def subframe(self):
		"""subframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subframe'):
			from .Subframe import SubframeCls
			self._subframe = SubframeCls(self._core, self._cmd_group)
		return self._subframe

	@property
	def ulIndex(self):
		"""ulIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulIndex'):
			from .UlIndex import UlIndexCls
			self._ulIndex = UlIndexCls(self._core, self._cmd_group)
		return self._ulIndex

	def clone(self) -> 'SeqElemCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SeqElemCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
