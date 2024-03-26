from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RmcCls:
	"""Rmc commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rmc", core, parent)

	@property
	def arBlocks(self):
		"""arBlocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_arBlocks'):
			from .ArBlocks import ArBlocksCls
			self._arBlocks = ArBlocksCls(self._core, self._cmd_group)
		return self._arBlocks

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def paySize(self):
		"""paySize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paySize'):
			from .PaySize import PaySizeCls
			self._paySize = PaySizeCls(self._core, self._cmd_group)
		return self._paySize

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .PhysBits import PhysBitsCls
			self._physBits = PhysBitsCls(self._core, self._cmd_group)
		return self._physBits

	@property
	def rmc(self):
		"""rmc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmc'):
			from .Rmc import RmcCls
			self._rmc = RmcCls(self._core, self._cmd_group)
		return self._rmc

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'RmcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RmcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
