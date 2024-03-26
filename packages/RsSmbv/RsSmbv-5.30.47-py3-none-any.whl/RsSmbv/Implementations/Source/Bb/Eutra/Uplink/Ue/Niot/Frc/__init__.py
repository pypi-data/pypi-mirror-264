from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrcCls:
	"""Frc commands group definition. 10 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frc", core, parent)

	@property
	def alResunits(self):
		"""alResunits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alResunits'):
			from .AlResunits import AlResunitsCls
			self._alResunits = AlResunitsCls(self._core, self._cmd_group)
		return self._alResunits

	@property
	def bpresUnit(self):
		"""bpresUnit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpresUnit'):
			from .BpresUnit import BpresUnitCls
			self._bpresUnit = BpresUnitCls(self._core, self._cmd_group)
		return self._bpresUnit

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def nnPrep(self):
		"""nnPrep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nnPrep'):
			from .NnPrep import NnPrepCls
			self._nnPrep = NnPrepCls(self._core, self._cmd_group)
		return self._nnPrep

	@property
	def nosCarriers(self):
		"""nosCarriers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nosCarriers'):
			from .NosCarriers import NosCarriersCls
			self._nosCarriers = NosCarriersCls(self._core, self._cmd_group)
		return self._nosCarriers

	@property
	def paSize(self):
		"""paSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paSize'):
			from .PaSize import PaSizeCls
			self._paSize = PaSizeCls(self._core, self._cmd_group)
		return self._paSize

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .ScSpacing import ScSpacingCls
			self._scSpacing = ScSpacingCls(self._core, self._cmd_group)
		return self._scSpacing

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tbssIndex(self):
		"""tbssIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbssIndex'):
			from .TbssIndex import TbssIndexCls
			self._tbssIndex = TbssIndexCls(self._core, self._cmd_group)
		return self._tbssIndex

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'FrcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
