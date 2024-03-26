from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L5BandCls:
	"""L5Band commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l5Band", core, parent)

	@property
	def b2A(self):
		"""b2A commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_b2A'):
			from .B2A import B2ACls
			self._b2A = B2ACls(self._core, self._cmd_group)
		return self._b2A

	@property
	def b2B(self):
		"""b2B commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_b2B'):
			from .B2B import B2BCls
			self._b2B = B2BCls(self._core, self._cmd_group)
		return self._b2B

	@property
	def b2I(self):
		"""b2I commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_b2I'):
			from .B2I import B2ICls
			self._b2I = B2ICls(self._core, self._cmd_group)
		return self._b2I

	def clone(self) -> 'L5BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L5BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
