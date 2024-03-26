from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CmodeCls:
	"""Cmode commands group definition. 8 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cmode", core, parent)

	@property
	def method(self):
		"""method commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_method'):
			from .Method import MethodCls
			self._method = MethodCls(self._core, self._cmd_group)
		return self._method

	@property
	def pattern(self):
		"""pattern commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Poffset import PoffsetCls
			self._poffset = PoffsetCls(self._core, self._cmd_group)
		return self._poffset

	@property
	def poMode(self):
		"""poMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poMode'):
			from .PoMode import PoModeCls
			self._poMode = PoModeCls(self._core, self._cmd_group)
		return self._poMode

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'CmodeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CmodeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
