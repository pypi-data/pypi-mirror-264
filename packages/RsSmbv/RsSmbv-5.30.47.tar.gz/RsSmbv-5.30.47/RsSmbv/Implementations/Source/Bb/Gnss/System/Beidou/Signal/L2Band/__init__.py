from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L2BandCls:
	"""L2Band commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l2Band", core, parent)

	@property
	def b3I(self):
		"""b3I commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_b3I'):
			from .B3I import B3ICls
			self._b3I = B3ICls(self._core, self._cmd_group)
		return self._b3I

	def clone(self) -> 'L2BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L2BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
