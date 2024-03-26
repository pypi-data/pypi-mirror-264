from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcodingCls:
	"""Ccoding commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ccoding", core, parent)

	@property
	def icqiOffset(self):
		"""icqiOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icqiOffset'):
			from .IcqiOffset import IcqiOffsetCls
			self._icqiOffset = IcqiOffsetCls(self._core, self._cmd_group)
		return self._icqiOffset

	@property
	def iharqOffset(self):
		"""iharqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iharqOffset'):
			from .IharqOffset import IharqOffsetCls
			self._iharqOffset = IharqOffsetCls(self._core, self._cmd_group)
		return self._iharqOffset

	@property
	def iriOffset(self):
		"""iriOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iriOffset'):
			from .IriOffset import IriOffsetCls
			self._iriOffset = IriOffsetCls(self._core, self._cmd_group)
		return self._iriOffset

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def ocqiMin(self):
		"""ocqiMin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ocqiMin'):
			from .OcqiMin import OcqiMinCls
			self._ocqiMin = OcqiMinCls(self._core, self._cmd_group)
		return self._ocqiMin

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'CcodingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CcodingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
