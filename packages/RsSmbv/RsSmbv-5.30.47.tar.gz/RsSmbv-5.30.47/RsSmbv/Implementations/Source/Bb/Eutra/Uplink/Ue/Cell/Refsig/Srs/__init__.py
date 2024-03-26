from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrsCls:
	"""Srs commands group definition. 16 total commands, 16 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("srs", core, parent)

	@property
	def bhop(self):
		"""bhop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bhop'):
			from .Bhop import BhopCls
			self._bhop = BhopCls(self._core, self._cmd_group)
		return self._bhop

	@property
	def bsrs(self):
		"""bsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsrs'):
			from .Bsrs import BsrsCls
			self._bsrs = BsrsCls(self._core, self._cmd_group)
		return self._bsrs

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .CycShift import CycShiftCls
			self._cycShift = CycShiftCls(self._core, self._cmd_group)
		return self._cycShift

	@property
	def isrs(self):
		"""isrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isrs'):
			from .Isrs import IsrsCls
			self._isrs = IsrsCls(self._core, self._cmd_group)
		return self._isrs

	@property
	def naPort(self):
		"""naPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naPort'):
			from .NaPort import NaPortCls
			self._naPort = NaPortCls(self._core, self._cmd_group)
		return self._naPort

	@property
	def nktc(self):
		"""nktc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nktc'):
			from .Nktc import NktcCls
			self._nktc = NktcCls(self._core, self._cmd_group)
		return self._nktc

	@property
	def nrrc(self):
		"""nrrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrrc'):
			from .Nrrc import NrrcCls
			self._nrrc = NrrcCls(self._core, self._cmd_group)
		return self._nrrc

	@property
	def ntrans(self):
		"""ntrans commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntrans'):
			from .Ntrans import NtransCls
			self._ntrans = NtransCls(self._core, self._cmd_group)
		return self._ntrans

	@property
	def powOffset(self):
		"""powOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_powOffset'):
			from .PowOffset import PowOffsetCls
			self._powOffset = PowOffsetCls(self._core, self._cmd_group)
		return self._powOffset

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def subf(self):
		"""subf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subf'):
			from .Subf import SubfCls
			self._subf = SubfCls(self._core, self._cmd_group)
		return self._subf

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Toffset import ToffsetCls
			self._toffset = ToffsetCls(self._core, self._cmd_group)
		return self._toffset

	@property
	def trComb(self):
		"""trComb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trComb'):
			from .TrComb import TrCombCls
			self._trComb = TrCombCls(self._core, self._cmd_group)
		return self._trComb

	@property
	def tsrs(self):
		"""tsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsrs'):
			from .Tsrs import TsrsCls
			self._tsrs = TsrsCls(self._core, self._cmd_group)
		return self._tsrs

	@property
	def tt0(self):
		"""tt0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tt0'):
			from .Tt0 import Tt0Cls
			self._tt0 = Tt0Cls(self._core, self._cmd_group)
		return self._tt0

	@property
	def upptsadd(self):
		"""upptsadd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_upptsadd'):
			from .Upptsadd import UpptsaddCls
			self._upptsadd = UpptsaddCls(self._core, self._cmd_group)
		return self._upptsadd

	def clone(self) -> 'SrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
