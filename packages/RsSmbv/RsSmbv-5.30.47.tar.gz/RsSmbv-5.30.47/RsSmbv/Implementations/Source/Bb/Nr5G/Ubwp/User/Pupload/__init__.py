from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuploadCls:
	"""Pupload commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pupload", core, parent)

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .Dlist import DlistCls
			self._dlist = DlistCls(self._core, self._cmd_group)
		return self._dlist

	@property
	def dsUnique(self):
		"""dsUnique commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsUnique'):
			from .DsUnique import DsUniqueCls
			self._dsUnique = DsUniqueCls(self._core, self._cmd_group)
		return self._dsUnique

	@property
	def initPattern(self):
		"""initPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_initPattern'):
			from .InitPattern import InitPatternCls
			self._initPattern = InitPatternCls(self._core, self._cmd_group)
		return self._initPattern

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	def clone(self) -> 'PuploadCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PuploadCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
