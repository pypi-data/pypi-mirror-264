from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NiotCls:
	"""Niot commands group definition. 12 total commands, 12 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("niot", core, parent)

	@property
	def cell(self):
		"""cell commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	@property
	def cidGroup(self):
		"""cidGroup commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cidGroup'):
			from .CidGroup import CidGroupCls
			self._cidGroup = CidGroupCls(self._core, self._cmd_group)
		return self._cidGroup

	@property
	def crsSeq(self):
		"""crsSeq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crsSeq'):
			from .CrsSeq import CrsSeqCls
			self._crsSeq = CrsSeqCls(self._core, self._cmd_group)
		return self._crsSeq

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Dfreq import DfreqCls
			self._dfreq = DfreqCls(self._core, self._cmd_group)
		return self._dfreq

	@property
	def gbrbIdx(self):
		"""gbrbIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gbrbIdx'):
			from .GbrbIdx import GbrbIdxCls
			self._gbrbIdx = GbrbIdxCls(self._core, self._cmd_group)
		return self._gbrbIdx

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def nvsf(self):
		"""nvsf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nvsf'):
			from .Nvsf import NvsfCls
			self._nvsf = NvsfCls(self._core, self._cmd_group)
		return self._nvsf

	@property
	def rbIdx(self):
		"""rbIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIdx'):
			from .RbIdx import RbIdxCls
			self._rbIdx = RbIdxCls(self._core, self._cmd_group)
		return self._rbIdx

	@property
	def sf(self):
		"""sf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sf'):
			from .Sf import SfCls
			self._sf = SfCls(self._core, self._cmd_group)
		return self._sf

	@property
	def sfall(self):
		"""sfall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfall'):
			from .Sfall import SfallCls
			self._sfall = SfallCls(self._core, self._cmd_group)
		return self._sfall

	@property
	def sfnn(self):
		"""sfnn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfnn'):
			from .Sfnn import SfnnCls
			self._sfnn = SfnnCls(self._core, self._cmd_group)
		return self._sfnn

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'NiotCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NiotCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
