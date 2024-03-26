from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PracCls:
	"""Prac commands group definition. 19 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prac", core, parent)

	@property
	def msg(self):
		"""msg commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_msg'):
			from .Msg import MsgCls
			self._msg = MsgCls(self._core, self._cmd_group)
		return self._msg

	@property
	def pts(self):
		"""pts commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_pts'):
			from .Pts import PtsCls
			self._pts = PtsCls(self._core, self._cmd_group)
		return self._pts

	@property
	def slength(self):
		"""slength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Slength import SlengthCls
			self._slength = SlengthCls(self._core, self._cmd_group)
		return self._slength

	def clone(self) -> 'PracCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PracCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
