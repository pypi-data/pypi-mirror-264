from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CategoryCls:
	"""Category commands group definition. 46 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("category", core, parent)

	@property
	def satellite(self):
		"""satellite commands group. 4 Sub-classes, 17 commands."""
		if not hasattr(self, '_satellite'):
			from .Satellite import SatelliteCls
			self._satellite = SatelliteCls(self._core, self._cmd_group)
		return self._satellite

	@property
	def umotion(self):
		"""umotion commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_umotion'):
			from .Umotion import UmotionCls
			self._umotion = UmotionCls(self._core, self._cmd_group)
		return self._umotion

	def clone(self) -> 'CategoryCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CategoryCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
