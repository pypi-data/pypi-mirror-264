from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FullCls:
	"""Full commands group definition. 11 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("full", core, parent)

	@property
	def area(self):
		"""area commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_area'):
			from .Area import AreaCls
			self._area = AreaCls(self._core, self._cmd_group)
		return self._area

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	@property
	def rwindow(self):
		"""rwindow commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_rwindow'):
			from .Rwindow import RwindowCls
			self._rwindow = RwindowCls(self._core, self._cmd_group)
		return self._rwindow

	@property
	def scale(self):
		"""scale commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scale'):
			from .Scale import ScaleCls
			self._scale = ScaleCls(self._core, self._cmd_group)
		return self._scale

	def clone(self) -> 'FullCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FullCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
