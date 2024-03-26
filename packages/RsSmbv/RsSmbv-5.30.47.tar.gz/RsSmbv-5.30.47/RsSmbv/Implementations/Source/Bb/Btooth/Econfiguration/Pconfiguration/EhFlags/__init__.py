from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EhFlagsCls:
	"""EhFlags commands group definition. 7 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ehFlags", core, parent)

	@property
	def aaddress(self):
		"""aaddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aaddress'):
			from .Aaddress import AaddressCls
			self._aaddress = AaddressCls(self._core, self._cmd_group)
		return self._aaddress

	@property
	def adInfo(self):
		"""adInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adInfo'):
			from .AdInfo import AdInfoCls
			self._adInfo = AdInfoCls(self._core, self._cmd_group)
		return self._adInfo

	@property
	def aptr(self):
		"""aptr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aptr'):
			from .Aptr import AptrCls
			self._aptr = AptrCls(self._core, self._cmd_group)
		return self._aptr

	@property
	def cinfo(self):
		"""cinfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cinfo'):
			from .Cinfo import CinfoCls
			self._cinfo = CinfoCls(self._core, self._cmd_group)
		return self._cinfo

	@property
	def sinfo(self):
		"""sinfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinfo'):
			from .Sinfo import SinfoCls
			self._sinfo = SinfoCls(self._core, self._cmd_group)
		return self._sinfo

	@property
	def taddress(self):
		"""taddress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taddress'):
			from .Taddress import TaddressCls
			self._taddress = TaddressCls(self._core, self._cmd_group)
		return self._taddress

	@property
	def tpower(self):
		"""tpower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpower'):
			from .Tpower import TpowerCls
			self._tpower = TpowerCls(self._core, self._cmd_group)
		return self._tpower

	def clone(self) -> 'EhFlagsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EhFlagsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
