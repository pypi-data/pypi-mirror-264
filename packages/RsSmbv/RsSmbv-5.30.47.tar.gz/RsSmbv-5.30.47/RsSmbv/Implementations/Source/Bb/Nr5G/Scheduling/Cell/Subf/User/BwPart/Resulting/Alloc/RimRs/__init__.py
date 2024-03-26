from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RimRsCls:
	"""RimRs commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rimRs", core, parent)

	@property
	def delta(self):
		"""delta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delta'):
			from .Delta import DeltaCls
			self._delta = DeltaCls(self._core, self._cmd_group)
		return self._delta

	@property
	def gamma(self):
		"""gamma commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gamma'):
			from .Gamma import GammaCls
			self._gamma = GammaCls(self._core, self._cmd_group)
		return self._gamma

	@property
	def ntrim(self):
		"""ntrim commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntrim'):
			from .Ntrim import NtrimCls
			self._ntrim = NtrimCls(self._core, self._cmd_group)
		return self._ntrim

	@property
	def scid(self):
		"""scid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scid'):
			from .Scid import ScidCls
			self._scid = ScidCls(self._core, self._cmd_group)
		return self._scid

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .ScSpacing import ScSpacingCls
			self._scSpacing = ScSpacingCls(self._core, self._cmd_group)
		return self._scSpacing

	def clone(self) -> 'RimRsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RimRsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
