from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NiotCls:
	"""Niot commands group definition. 41 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("niot", core, parent)

	@property
	def arb(self):
		"""arb commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_arb'):
			from .Arb import ArbCls
			self._arb = ArbCls(self._core, self._cmd_group)
		return self._arb

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Dfreq import DfreqCls
			self._dfreq = DfreqCls(self._core, self._cmd_group)
		return self._dfreq

	@property
	def frc(self):
		"""frc commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_frc'):
			from .Frc import FrcCls
			self._frc = FrcCls(self._core, self._cmd_group)
		return self._frc

	@property
	def ghDisable(self):
		"""ghDisable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ghDisable'):
			from .GhDisable import GhDisableCls
			self._ghDisable = GhDisableCls(self._core, self._cmd_group)
		return self._ghDisable

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def npssim(self):
		"""npssim commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npssim'):
			from .Npssim import NpssimCls
			self._npssim = NpssimCls(self._core, self._cmd_group)
		return self._npssim

	@property
	def ntransmiss(self):
		"""ntransmiss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransmiss'):
			from .Ntransmiss import NtransmissCls
			self._ntransmiss = NtransmissCls(self._core, self._cmd_group)
		return self._ntransmiss

	@property
	def rbIndex(self):
		"""rbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIndex'):
			from .RbIndex import RbIndexCls
			self._rbIndex = RbIndexCls(self._core, self._cmd_group)
		return self._rbIndex

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .ScSpacing import ScSpacingCls
			self._scSpacing = ScSpacingCls(self._core, self._cmd_group)
		return self._scSpacing

	@property
	def trans(self):
		"""trans commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_trans'):
			from .Trans import TransCls
			self._trans = TransCls(self._core, self._cmd_group)
		return self._trans

	def clone(self) -> 'NiotCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NiotCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
