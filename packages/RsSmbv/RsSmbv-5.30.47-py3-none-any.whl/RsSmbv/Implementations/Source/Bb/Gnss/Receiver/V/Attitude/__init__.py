from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AttitudeCls:
	"""Attitude commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attitude", core, parent)

	@property
	def pitch(self):
		"""pitch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pitch'):
			from .Pitch import PitchCls
			self._pitch = PitchCls(self._core, self._cmd_group)
		return self._pitch

	@property
	def roll(self):
		"""roll commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_roll'):
			from .Roll import RollCls
			self._roll = RollCls(self._core, self._cmd_group)
		return self._roll

	@property
	def spin(self):
		"""spin commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spin'):
			from .Spin import SpinCls
			self._spin = SpinCls(self._core, self._cmd_group)
		return self._spin

	@property
	def yaw(self):
		"""yaw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yaw'):
			from .Yaw import YawCls
			self._yaw = YawCls(self._core, self._cmd_group)
		return self._yaw

	@property
	def behaviour(self):
		"""behaviour commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_behaviour'):
			from .Behaviour import BehaviourCls
			self._behaviour = BehaviourCls(self._core, self._cmd_group)
		return self._behaviour

	def clone(self) -> 'AttitudeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AttitudeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
