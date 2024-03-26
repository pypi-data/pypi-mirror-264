from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReceiverCls:
	"""Receiver commands group definition. 81 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("receiver", core, parent)

	@property
	def v(self):
		"""v commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_v'):
			from .V import VCls
			self._v = VCls(self._core, self._cmd_group)
		return self._v

	def clone(self) -> 'ReceiverCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ReceiverCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
