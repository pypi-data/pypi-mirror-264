from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HilCls:
	"""Hil commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hil", core, parent)

	@property
	def itype(self):
		"""itype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_itype'):
			from .Itype import ItypeCls
			self._itype = ItypeCls(self._core, self._cmd_group)
		return self._itype

	@property
	def port(self):
		"""port commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_port'):
			from .Port import PortCls
			self._port = PortCls(self._core, self._cmd_group)
		return self._port

	@property
	def slatency(self):
		"""slatency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slatency'):
			from .Slatency import SlatencyCls
			self._slatency = SlatencyCls(self._core, self._cmd_group)
		return self._slatency

	def clone(self) -> 'HilCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HilCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
