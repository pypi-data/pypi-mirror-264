from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SequenceCls:
	"""Sequence commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sequence", core, parent)

	@property
	def increment(self):
		"""increment commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_increment'):
			from .Increment import IncrementCls
			self._increment = IncrementCls(self._core, self._cmd_group)
		return self._increment

	@property
	def start(self):
		"""start commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_start'):
			from .Start import StartCls
			self._start = StartCls(self._core, self._cmd_group)
		return self._start

	def clone(self) -> 'SequenceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SequenceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
