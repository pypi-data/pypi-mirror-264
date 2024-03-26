from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CkeyCls:
	"""Ckey commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ckey", core, parent)

	@property
	def tduration(self):
		"""tduration commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tduration'):
			from .Tduration import TdurationCls
			self._tduration = TdurationCls(self._core, self._cmd_group)
		return self._tduration

	def clone(self) -> 'CkeyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CkeyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
