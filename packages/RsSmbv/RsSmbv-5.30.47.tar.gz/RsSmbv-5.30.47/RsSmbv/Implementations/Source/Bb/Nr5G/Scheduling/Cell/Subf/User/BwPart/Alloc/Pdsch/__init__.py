from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PdschCls:
	"""Pdsch commands group definition. 38 total commands, 11 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdsch", core, parent)

	@property
	def bmaid(self):
		"""bmaid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmaid'):
			from .Bmaid import BmaidCls
			self._bmaid = BmaidCls(self._core, self._cmd_group)
		return self._bmaid

	@property
	def dmr(self):
		"""dmr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmr'):
			from .Dmr import DmrCls
			self._dmr = DmrCls(self._core, self._cmd_group)
		return self._dmr

	@property
	def dmrs(self):
		"""dmrs commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Dmrs import DmrsCls
			self._dmrs = DmrsCls(self._core, self._cmd_group)
		return self._dmrs

	@property
	def ncw(self):
		"""ncw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncw'):
			from .Ncw import NcwCls
			self._ncw = NcwCls(self._core, self._cmd_group)
		return self._ncw

	@property
	def patgrp(self):
		"""patgrp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_patgrp'):
			from .Patgrp import PatgrpCls
			self._patgrp = PatgrpCls(self._core, self._cmd_group)
		return self._patgrp

	@property
	def precg(self):
		"""precg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_precg'):
			from .Precg import PrecgCls
			self._precg = PrecgCls(self._core, self._cmd_group)
		return self._precg

	@property
	def ptrs(self):
		"""ptrs commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptrs'):
			from .Ptrs import PtrsCls
			self._ptrs = PtrsCls(self._core, self._cmd_group)
		return self._ptrs

	@property
	def resAlloc(self):
		"""resAlloc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_resAlloc'):
			from .ResAlloc import ResAllocCls
			self._resAlloc = ResAllocCls(self._core, self._cmd_group)
		return self._resAlloc

	@property
	def sbcZero(self):
		"""sbcZero commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbcZero'):
			from .SbcZero import SbcZeroCls
			self._sbcZero = SbcZeroCls(self._core, self._cmd_group)
		return self._sbcZero

	@property
	def txScheme(self):
		"""txScheme commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_txScheme'):
			from .TxScheme import TxSchemeCls
			self._txScheme = TxSchemeCls(self._core, self._cmd_group)
		return self._txScheme

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'PdschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PdschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
