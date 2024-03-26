from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrcCls:
	"""Frc commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frc", core, parent)

	@property
	def alrb(self):
		"""alrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alrb'):
			from .Alrb import AlrbCls
			self._alrb = AlrbCls(self._core, self._cmd_group)
		return self._alrb

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def n2Dmrs(self):
		"""n2Dmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Dmrs'):
			from .N2Dmrs import N2DmrsCls
			self._n2Dmrs = N2DmrsCls(self._core, self._cmd_group)
		return self._n2Dmrs

	@property
	def paSize(self):
		"""paSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paSize'):
			from .PaSize import PaSizeCls
			self._paSize = PaSizeCls(self._core, self._cmd_group)
		return self._paSize

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tnoBits(self):
		"""tnoBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tnoBits'):
			from .TnoBits import TnoBitsCls
			self._tnoBits = TnoBitsCls(self._core, self._cmd_group)
		return self._tnoBits

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def vrbOffset(self):
		"""vrbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vrbOffset'):
			from .VrbOffset import VrbOffsetCls
			self._vrbOffset = VrbOffsetCls(self._core, self._cmd_group)
		return self._vrbOffset

	def clone(self) -> 'FrcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
