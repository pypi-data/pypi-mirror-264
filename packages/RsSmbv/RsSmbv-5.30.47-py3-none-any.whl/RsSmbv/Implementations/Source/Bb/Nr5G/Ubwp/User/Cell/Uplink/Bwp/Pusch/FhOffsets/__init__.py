from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FhOffsetsCls:
	"""FhOffsets commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fhOffsets", core, parent)

	@property
	def noffsets(self):
		"""noffsets commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noffsets'):
			from .Noffsets import NoffsetsCls
			self._noffsets = NoffsetsCls(self._core, self._cmd_group)
		return self._noffsets

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	def clone(self) -> 'FhOffsetsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FhOffsetsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
