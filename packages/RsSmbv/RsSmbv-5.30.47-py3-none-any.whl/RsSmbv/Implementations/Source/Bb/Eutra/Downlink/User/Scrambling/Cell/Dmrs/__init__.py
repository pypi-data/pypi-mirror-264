from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmrsCls:
	"""Dmrs commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmrs", core, parent)

	@property
	def id1(self):
		"""id1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id1'):
			from .Id1 import Id1Cls
			self._id1 = Id1Cls(self._core, self._cmd_group)
		return self._id1

	@property
	def id2(self):
		"""id2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id2'):
			from .Id2 import Id2Cls
			self._id2 = Id2Cls(self._core, self._cmd_group)
		return self._id2

	@property
	def use(self):
		"""use commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_use'):
			from .Use import UseCls
			self._use = UseCls(self._core, self._cmd_group)
		return self._use

	def clone(self) -> 'DmrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
