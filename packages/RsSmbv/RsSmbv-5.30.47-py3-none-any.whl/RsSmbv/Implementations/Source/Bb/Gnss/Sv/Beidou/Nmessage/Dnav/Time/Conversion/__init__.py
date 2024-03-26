from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConversionCls:
	"""Conversion commands group definition. 28 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("conversion", core, parent)

	@property
	def galileo(self):
		"""galileo commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_glonass'):
			from .Glonass import GlonassCls
			self._glonass = GlonassCls(self._core, self._cmd_group)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_gps'):
			from .Gps import GpsCls
			self._gps = GpsCls(self._core, self._cmd_group)
		return self._gps

	@property
	def utc(self):
		"""utc commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_utc'):
			from .Utc import UtcCls
			self._utc = UtcCls(self._core, self._cmd_group)
		return self._utc

	def clone(self) -> 'ConversionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConversionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
