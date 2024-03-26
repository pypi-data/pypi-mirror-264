from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectorCls:
	"""Connector commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connector", core, parent)

	@property
	def bsin(self):
		"""bsin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsin'):
			from .Bsin import BsinCls
			self._bsin = BsinCls(self._core, self._cmd_group)
		return self._bsin

	@property
	def bsout(self):
		"""bsout commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsout'):
			from .Bsout import BsoutCls
			self._bsout = BsoutCls(self._core, self._cmd_group)
		return self._bsout

	def clone(self) -> 'ConnectorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConnectorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
