from ...............Internal.Core import Core
from ...............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqCls:
	"""Seq commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seq", core, parent)

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .CycShift import CycShiftCls
			self._cycShift = CycShiftCls(self._core, self._cmd_group)
		return self._cycShift

	@property
	def hopping(self):
		"""hopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopping'):
			from .Hopping import HoppingCls
			self._hopping = HoppingCls(self._core, self._cmd_group)
		return self._hopping

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	def clone(self) -> 'SeqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SeqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
