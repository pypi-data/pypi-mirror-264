from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnhCls:
	"""Enh commands group definition. 106 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enh", core, parent)

	@property
	def bch(self):
		"""bch commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_bch'):
			from .Bch import BchCls
			self._bch = BchCls(self._core, self._cmd_group)
		return self._bch

	@property
	def dch(self):
		"""dch commands group. 17 Sub-classes, 0 commands."""
		if not hasattr(self, '_dch'):
			from .Dch import DchCls
			self._dch = DchCls(self._core, self._cmd_group)
		return self._dch

	def clone(self) -> 'EnhCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EnhCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
