from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdpchCls:
	"""Fdpch commands group definition. 6 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdpch", core, parent)

	@property
	def dpcch(self):
		"""dpcch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpcch'):
			from .Dpcch import DpcchCls
			self._dpcch = DpcchCls(self._core, self._cmd_group)
		return self._dpcch

	def clone(self) -> 'FdpchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FdpchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
