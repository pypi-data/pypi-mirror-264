from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScontrolCls:
	"""Scontrol commands group definition. 5 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scontrol", core, parent)

	@property
	def fragment(self):
		"""fragment commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fragment'):
			from .Fragment import FragmentCls
			self._fragment = FragmentCls(self._core, self._cmd_group)
		return self._fragment

	@property
	def sequence(self):
		"""sequence commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequence'):
			from .Sequence import SequenceCls
			self._sequence = SequenceCls(self._core, self._cmd_group)
		return self._sequence

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'ScontrolCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScontrolCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
