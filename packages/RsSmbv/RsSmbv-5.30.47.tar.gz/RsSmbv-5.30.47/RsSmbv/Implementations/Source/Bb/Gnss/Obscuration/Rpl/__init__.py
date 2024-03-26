from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RplCls:
	"""Rpl commands group definition. 2 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rpl", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	def clone(self) -> 'RplCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RplCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
