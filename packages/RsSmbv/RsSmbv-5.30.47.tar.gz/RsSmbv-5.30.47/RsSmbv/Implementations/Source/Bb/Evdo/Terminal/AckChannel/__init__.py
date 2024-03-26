from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AckChannelCls:
	"""AckChannel commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ackChannel", core, parent)

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def gating(self):
		"""gating commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gating'):
			from .Gating import GatingCls
			self._gating = GatingCls(self._core, self._cmd_group)
		return self._gating

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def values(self):
		"""values commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_values'):
			from .Values import ValuesCls
			self._values = ValuesCls(self._core, self._cmd_group)
		return self._values

	def clone(self) -> 'AckChannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AckChannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
