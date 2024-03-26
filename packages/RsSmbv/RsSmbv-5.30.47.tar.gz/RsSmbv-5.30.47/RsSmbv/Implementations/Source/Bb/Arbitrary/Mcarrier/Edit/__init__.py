from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EditCls:
	"""Edit commands group definition. 11 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("edit", core, parent)

	@property
	def carrier(self):
		"""carrier commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_carrier'):
			from .Carrier import CarrierCls
			self._carrier = CarrierCls(self._core, self._cmd_group)
		return self._carrier

	def clone(self) -> 'EditCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EditCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
