from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GsrCls:
	"""Gsr commands group definition. 11 total commands, 11 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gsr", core, parent)

	@property
	def conductivity(self):
		"""conductivity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conductivity'):
			from .Conductivity import ConductivityCls
			self._conductivity = ConductivityCls(self._core, self._cmd_group)
		return self._conductivity

	@property
	def galtitude(self):
		"""galtitude commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_galtitude'):
			from .Galtitude import GaltitudeCls
			self._galtitude = GaltitudeCls(self._core, self._cmd_group)
		return self._galtitude

	@property
	def mproperty(self):
		"""mproperty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mproperty'):
			from .Mproperty import MpropertyCls
			self._mproperty = MpropertyCls(self._core, self._cmd_group)
		return self._mproperty

	@property
	def o1Distance(self):
		"""o1Distance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_o1Distance'):
			from .O1Distance import O1DistanceCls
			self._o1Distance = O1DistanceCls(self._core, self._cmd_group)
		return self._o1Distance

	@property
	def o1Height(self):
		"""o1Height commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_o1Height'):
			from .O1Height import O1HeightCls
			self._o1Height = O1HeightCls(self._core, self._cmd_group)
		return self._o1Height

	@property
	def o2Distance(self):
		"""o2Distance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_o2Distance'):
			from .O2Distance import O2DistanceCls
			self._o2Distance = O2DistanceCls(self._core, self._cmd_group)
		return self._o2Distance

	@property
	def o2Height(self):
		"""o2Height commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_o2Height'):
			from .O2Height import O2HeightCls
			self._o2Height = O2HeightCls(self._core, self._cmd_group)
		return self._o2Height

	@property
	def oorientation(self):
		"""oorientation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oorientation'):
			from .Oorientation import OorientationCls
			self._oorientation = OorientationCls(self._core, self._cmd_group)
		return self._oorientation

	@property
	def permittivity(self):
		"""permittivity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_permittivity'):
			from .Permittivity import PermittivityCls
			self._permittivity = PermittivityCls(self._core, self._cmd_group)
		return self._permittivity

	@property
	def ploss(self):
		"""ploss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ploss'):
			from .Ploss import PlossCls
			self._ploss = PlossCls(self._core, self._cmd_group)
		return self._ploss

	@property
	def stype(self):
		"""stype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stype'):
			from .Stype import StypeCls
			self._stype = StypeCls(self._core, self._cmd_group)
		return self._stype

	def clone(self) -> 'GsrCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GsrCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
