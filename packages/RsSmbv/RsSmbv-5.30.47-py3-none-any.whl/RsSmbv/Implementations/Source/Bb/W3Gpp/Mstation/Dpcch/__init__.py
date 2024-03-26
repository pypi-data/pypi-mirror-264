from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpcchCls:
	"""Dpcch commands group definition. 60 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpcch", core, parent)

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .Ccode import CcodeCls
			self._ccode = CcodeCls(self._core, self._cmd_group)
		return self._ccode

	@property
	def fbi(self):
		"""fbi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fbi'):
			from .Fbi import FbiCls
			self._fbi = FbiCls(self._core, self._cmd_group)
		return self._fbi

	@property
	def hs(self):
		"""hs commands group. 20 Sub-classes, 0 commands."""
		if not hasattr(self, '_hs'):
			from .Hs import HsCls
			self._hs = HsCls(self._core, self._cmd_group)
		return self._hs

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def tfci(self):
		"""tfci commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .Tfci import TfciCls
			self._tfci = TfciCls(self._core, self._cmd_group)
		return self._tfci

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Toffset import ToffsetCls
			self._toffset = ToffsetCls(self._core, self._cmd_group)
		return self._toffset

	@property
	def tpc(self):
		"""tpc commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Tpc import TpcCls
			self._tpc = TpcCls(self._core, self._cmd_group)
		return self._tpc

	def clone(self) -> 'DpcchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpcchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
