from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NiotCls:
	"""Niot commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

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
	def mod(self):
		"""mod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mod'):
			from .Mod import ModCls
			self._mod = ModCls(self._core, self._cmd_group)
		return self._mod

	@property
	def prAttempts(self):
		"""prAttempts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prAttempts'):
			from .PrAttempts import PrAttemptsCls
			self._prAttempts = PrAttemptsCls(self._core, self._cmd_group)
		return self._prAttempts

	@property
	def rbid(self):
		"""rbid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbid'):
			from .Rbid import RbidCls
			self._rbid = RbidCls(self._core, self._cmd_group)
		return self._rbid

	def clone(self) -> 'NiotCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NiotCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
