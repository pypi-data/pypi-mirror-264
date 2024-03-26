from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TfConfigCls:
	"""TfConfig commands group definition. 40 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tfConfig", core, parent)

	@property
	def cinfo(self):
		"""cinfo commands group. 20 Sub-classes, 0 commands."""
		if not hasattr(self, '_cinfo'):
			from .Cinfo import CinfoCls
			self._cinfo = CinfoCls(self._core, self._cmd_group)
		return self._cinfo

	@property
	def eof(self):
		"""eof commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eof'):
			from .Eof import EofCls
			self._eof = EofCls(self._core, self._cmd_group)
		return self._eof

	@property
	def nuInfo(self):
		"""nuInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nuInfo'):
			from .NuInfo import NuInfoCls
			self._nuInfo = NuInfoCls(self._core, self._cmd_group)
		return self._nuInfo

	@property
	def padLength(self):
		"""padLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_padLength'):
			from .PadLength import PadLengthCls
			self._padLength = PadLengthCls(self._core, self._cmd_group)
		return self._padLength

	@property
	def tpTime(self):
		"""tpTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpTime'):
			from .TpTime import TpTimeCls
			self._tpTime = TpTimeCls(self._core, self._cmd_group)
		return self._tpTime

	@property
	def uinfo(self):
		"""uinfo commands group. 16 Sub-classes, 0 commands."""
		if not hasattr(self, '_uinfo'):
			from .Uinfo import UinfoCls
			self._uinfo = UinfoCls(self._core, self._cmd_group)
		return self._uinfo

	def clone(self) -> 'TfConfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TfConfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
