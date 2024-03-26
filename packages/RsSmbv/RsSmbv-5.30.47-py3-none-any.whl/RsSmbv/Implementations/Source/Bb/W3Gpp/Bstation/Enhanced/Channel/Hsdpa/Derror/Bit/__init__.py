from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BitCls:
	"""Bit commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bit", core, parent)

	@property
	def layer(self):
		"""layer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_layer'):
			from .Layer import LayerCls
			self._layer = LayerCls(self._core, self._cmd_group)
		return self._layer

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Rate import RateCls
			self._rate = RateCls(self._core, self._cmd_group)
		return self._rate

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'BitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
