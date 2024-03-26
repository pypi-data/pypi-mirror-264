from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L2BandCls:
	"""L2Band commands group definition. 18 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l2Band", core, parent)

	@property
	def e6Prs(self):
		"""e6Prs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_e6Prs'):
			from .E6Prs import E6PrsCls
			self._e6Prs = E6PrsCls(self._core, self._cmd_group)
		return self._e6Prs

	@property
	def e6S(self):
		"""e6S commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_e6S'):
			from .E6S import E6SCls
			self._e6S = E6SCls(self._core, self._cmd_group)
		return self._e6S

	def clone(self) -> 'L2BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L2BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
