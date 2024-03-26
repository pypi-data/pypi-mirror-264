from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UplinkCls:
	"""Uplink commands group definition. 169 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uplink", core, parent)

	@property
	def bwp(self):
		"""bwp commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_bwp'):
			from .Bwp import BwpCls
			self._bwp = BwpCls(self._core, self._cmd_group)
		return self._bwp

	@property
	def nbwParts(self):
		"""nbwParts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nbwParts'):
			from .NbwParts import NbwPartsCls
			self._nbwParts = NbwPartsCls(self._core, self._cmd_group)
		return self._nbwParts

	def clone(self) -> 'UplinkCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UplinkCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
