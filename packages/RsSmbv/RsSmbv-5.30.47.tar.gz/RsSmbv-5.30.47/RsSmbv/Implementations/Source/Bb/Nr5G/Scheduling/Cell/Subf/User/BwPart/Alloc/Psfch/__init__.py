from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PsfchCls:
	"""Psfch commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("psfch", core, parent)

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .CycShift import CycShiftCls
			self._cycShift = CycShiftCls(self._core, self._cmd_group)
		return self._cycShift

	@property
	def harq(self):
		"""harq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def hopId(self):
		"""hopId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopId'):
			from .HopId import HopIdCls
			self._hopId = HopIdCls(self._core, self._cmd_group)
		return self._hopId

	@property
	def tran(self):
		"""tran commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tran'):
			from .Tran import TranCls
			self._tran = TranCls(self._core, self._cmd_group)
		return self._tran

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'PsfchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PsfchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
