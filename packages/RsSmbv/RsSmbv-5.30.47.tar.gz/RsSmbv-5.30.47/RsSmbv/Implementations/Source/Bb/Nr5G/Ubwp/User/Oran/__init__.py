from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OranCls:
	"""Oran commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("oran", core, parent)

	@property
	def tc(self):
		"""tc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tc'):
			from .Tc import TcCls
			self._tc = TcCls(self._core, self._cmd_group)
		return self._tc

	@property
	def usds(self):
		"""usds commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usds'):
			from .Usds import UsdsCls
			self._usds = UsdsCls(self._core, self._cmd_group)
		return self._usds

	def clone(self) -> 'OranCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OranCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
