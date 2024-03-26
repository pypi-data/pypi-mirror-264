from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmtbCls:
	"""Dmtb commands group definition. 14 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmtb", core, parent)

	@property
	def apIndex(self):
		"""apIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apIndex'):
			from .ApIndex import ApIndexCls
			self._apIndex = ApIndexCls(self._core, self._cmd_group)
		return self._apIndex

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .Ctype import CtypeCls
			self._ctype = CtypeCls(self._core, self._cmd_group)
		return self._ctype

	@property
	def mlength(self):
		"""mlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mlength'):
			from .Mlength import MlengthCls
			self._mlength = MlengthCls(self._core, self._cmd_group)
		return self._mlength

	@property
	def ptrs(self):
		"""ptrs commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptrs'):
			from .Ptrs import PtrsCls
			self._ptrs = PtrsCls(self._core, self._cmd_group)
		return self._ptrs

	@property
	def sid0(self):
		"""sid0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sid0'):
			from .Sid0 import Sid0Cls
			self._sid0 = Sid0Cls(self._core, self._cmd_group)
		return self._sid0

	@property
	def sid1(self):
		"""sid1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sid1'):
			from .Sid1 import Sid1Cls
			self._sid1 = Sid1Cls(self._core, self._cmd_group)
		return self._sid1

	@property
	def ur16(self):
		"""ur16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ur16'):
			from .Ur16 import Ur16Cls
			self._ur16 = Ur16Cls(self._core, self._cmd_group)
		return self._ur16

	def clone(self) -> 'DmtbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmtbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
