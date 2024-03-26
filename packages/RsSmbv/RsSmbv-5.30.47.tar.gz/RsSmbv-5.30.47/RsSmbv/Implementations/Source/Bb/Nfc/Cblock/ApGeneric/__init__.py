from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApGenericCls:
	"""ApGeneric commands group definition. 9 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apGeneric", core, parent)

	@property
	def bodata(self):
		"""bodata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bodata'):
			from .Bodata import BodataCls
			self._bodata = BodataCls(self._core, self._cmd_group)
		return self._bodata

	@property
	def boLength(self):
		"""boLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_boLength'):
			from .BoLength import BoLengthCls
			self._boLength = BoLengthCls(self._core, self._cmd_group)
		return self._boLength

	@property
	def ftype(self):
		"""ftype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ftype'):
			from .Ftype import FtypeCls
			self._ftype = FtypeCls(self._core, self._cmd_group)
		return self._ftype

	@property
	def shdata(self):
		"""shdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shdata'):
			from .Shdata import ShdataCls
			self._shdata = ShdataCls(self._core, self._cmd_group)
		return self._shdata

	@property
	def shLength(self):
		"""shLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shLength'):
			from .ShLength import ShLengthCls
			self._shLength = ShLengthCls(self._core, self._cmd_group)
		return self._shLength

	@property
	def stdLength(self):
		"""stdLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stdLength'):
			from .StdLength import StdLengthCls
			self._stdLength = StdLengthCls(self._core, self._cmd_group)
		return self._stdLength

	@property
	def stdata(self):
		"""stdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stdata'):
			from .Stdata import StdataCls
			self._stdata = StdataCls(self._core, self._cmd_group)
		return self._stdata

	@property
	def stePresent(self):
		"""stePresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stePresent'):
			from .StePresent import StePresentCls
			self._stePresent = StePresentCls(self._core, self._cmd_group)
		return self._stePresent

	@property
	def stpLength(self):
		"""stpLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stpLength'):
			from .StpLength import StpLengthCls
			self._stpLength = StpLengthCls(self._core, self._cmd_group)
		return self._stpLength

	def clone(self) -> 'ApGenericCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApGenericCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
