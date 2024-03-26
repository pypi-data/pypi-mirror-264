from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FcontrolCls:
	"""Fcontrol commands group definition. 7 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fcontrol", core, parent)

	@property
	def bindication(self):
		"""bindication commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bindication'):
			from .Bindication import BindicationCls
			self._bindication = BindicationCls(self._core, self._cmd_group)
		return self._bindication

	@property
	def dindication(self):
		"""dindication commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dindication'):
			from .Dindication import DindicationCls
			self._dindication = DindicationCls(self._core, self._cmd_group)
		return self._dindication

	@property
	def fcontrol(self):
		"""fcontrol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fcontrol'):
			from .Fcontrol import FcontrolCls
			self._fcontrol = FcontrolCls(self._core, self._cmd_group)
		return self._fcontrol

	@property
	def ntiPresent(self):
		"""ntiPresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntiPresent'):
			from .NtiPresent import NtiPresentCls
			self._ntiPresent = NtiPresentCls(self._core, self._cmd_group)
		return self._ntiPresent

	@property
	def pframe(self):
		"""pframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pframe'):
			from .Pframe import PframeCls
			self._pframe = PframeCls(self._core, self._cmd_group)
		return self._pframe

	@property
	def ptype(self):
		"""ptype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptype'):
			from .Ptype import PtypeCls
			self._ptype = PtypeCls(self._core, self._cmd_group)
		return self._ptype

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .Reserved import ReservedCls
			self._reserved = ReservedCls(self._core, self._cmd_group)
		return self._reserved

	def clone(self) -> 'FcontrolCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FcontrolCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
