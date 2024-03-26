from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZadCls:
	"""Zad commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zad", core, parent)

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .CycShift import CycShiftCls
			self._cycShift = CycShiftCls(self._core, self._cmd_group)
		return self._cycShift

	@property
	def slen(self):
		"""slen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slen'):
			from .Slen import SlenCls
			self._slen = SlenCls(self._core, self._cmd_group)
		return self._slen

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .Snumber import SnumberCls
			self._snumber = SnumberCls(self._core, self._cmd_group)
		return self._snumber

	def clone(self) -> 'ZadCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ZadCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
