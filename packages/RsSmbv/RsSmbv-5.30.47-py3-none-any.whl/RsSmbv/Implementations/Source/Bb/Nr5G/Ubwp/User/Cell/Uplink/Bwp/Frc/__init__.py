from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrcCls:
	"""Frc commands group definition. 20 total commands, 20 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frc", core, parent)

	@property
	def abw(self):
		"""abw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_abw'):
			from .Abw import AbwCls
			self._abw = AbwCls(self._core, self._cmd_group)
		return self._abw

	@property
	def alrb(self):
		"""alrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alrb'):
			from .Alrb import AlrbCls
			self._alrb = AlrbCls(self._core, self._cmd_group)
		return self._alrb

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Bw import BwCls
			self._bw = BwCls(self._core, self._cmd_group)
		return self._bw

	@property
	def mapType(self):
		"""mapType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapType'):
			from .MapType import MapTypeCls
			self._mapType = MapTypeCls(self._core, self._cmd_group)
		return self._mapType

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def paSize(self):
		"""paSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paSize'):
			from .PaSize import PaSizeCls
			self._paSize = PaSizeCls(self._core, self._cmd_group)
		return self._paSize

	@property
	def ptrs(self):
		"""ptrs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptrs'):
			from .Ptrs import PtrsCls
			self._ptrs = PtrsCls(self._core, self._cmd_group)
		return self._ptrs

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .RbOffset import RbOffsetCls
			self._rbOffset = RbOffsetCls(self._core, self._cmd_group)
		return self._rbOffset

	@property
	def scs(self):
		"""scs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scs'):
			from .Scs import ScsCls
			self._scs = ScsCls(self._core, self._cmd_group)
		return self._scs

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def walrb(self):
		"""walrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_walrb'):
			from .Walrb import WalrbCls
			self._walrb = WalrbCls(self._core, self._cmd_group)
		return self._walrb

	@property
	def wdeployment(self):
		"""wdeployment commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wdeployment'):
			from .Wdeployment import WdeploymentCls
			self._wdeployment = WdeploymentCls(self._core, self._cmd_group)
		return self._wdeployment

	@property
	def wmaType(self):
		"""wmaType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wmaType'):
			from .WmaType import WmaTypeCls
			self._wmaType = WmaTypeCls(self._core, self._cmd_group)
		return self._wmaType

	@property
	def wmodulation(self):
		"""wmodulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wmodulation'):
			from .Wmodulation import WmodulationCls
			self._wmodulation = WmodulationCls(self._core, self._cmd_group)
		return self._wmodulation

	@property
	def wpaSize(self):
		"""wpaSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wpaSize'):
			from .WpaSize import WpaSizeCls
			self._wpaSize = WpaSizeCls(self._core, self._cmd_group)
		return self._wpaSize

	@property
	def wptrs(self):
		"""wptrs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_wptrs'):
			from .Wptrs import WptrsCls
			self._wptrs = WptrsCls(self._core, self._cmd_group)
		return self._wptrs

	@property
	def wrOffset(self):
		"""wrOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wrOffset'):
			from .WrOffset import WrOffsetCls
			self._wrOffset = WrOffsetCls(self._core, self._cmd_group)
		return self._wrOffset

	@property
	def wscSpacing(self):
		"""wscSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wscSpacing'):
			from .WscSpacing import WscSpacingCls
			self._wscSpacing = WscSpacingCls(self._core, self._cmd_group)
		return self._wscSpacing

	@property
	def wtyp(self):
		"""wtyp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wtyp'):
			from .Wtyp import WtypCls
			self._wtyp = WtypCls(self._core, self._cmd_group)
		return self._wtyp

	def clone(self) -> 'FrcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
