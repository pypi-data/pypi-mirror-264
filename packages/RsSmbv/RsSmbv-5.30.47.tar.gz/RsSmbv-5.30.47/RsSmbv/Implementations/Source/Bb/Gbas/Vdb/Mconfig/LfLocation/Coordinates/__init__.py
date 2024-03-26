from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoordinatesCls:
	"""Coordinates commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coordinates", core, parent)

	@property
	def decimal(self):
		"""decimal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_decimal'):
			from .Decimal import DecimalCls
			self._decimal = DecimalCls(self._core, self._cmd_group)
		return self._decimal

	@property
	def dms(self):
		"""dms commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dms'):
			from .Dms import DmsCls
			self._dms = DmsCls(self._core, self._cmd_group)
		return self._dms

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	def clone(self) -> 'CoordinatesCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CoordinatesCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
