from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NpdschCls:
	"""Npdsch commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("npdsch", core, parent)

	@property
	def irep(self):
		"""irep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_irep'):
			from .Irep import IrepCls
			self._irep = IrepCls(self._core, self._cmd_group)
		return self._irep

	@property
	def isf(self):
		"""isf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isf'):
			from .Isf import IsfCls
			self._isf = IsfCls(self._core, self._cmd_group)
		return self._isf

	@property
	def nrep(self):
		"""nrep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrep'):
			from .Nrep import NrepCls
			self._nrep = NrepCls(self._core, self._cmd_group)
		return self._nrep

	@property
	def nsf(self):
		"""nsf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsf'):
			from .Nsf import NsfCls
			self._nsf = NsfCls(self._core, self._cmd_group)
		return self._nsf

	def clone(self) -> 'NpdschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NpdschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
