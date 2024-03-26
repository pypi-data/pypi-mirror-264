from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AtmosphericCls:
	"""Atmospheric commands group definition. 71 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("atmospheric", core, parent)

	@property
	def beidou(self):
		"""beidou commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Beidou import BeidouCls
			self._beidou = BeidouCls(self._core, self._cmd_group)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def gps(self):
		"""gps commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Gps import GpsCls
			self._gps = GpsCls(self._core, self._cmd_group)
		return self._gps

	@property
	def ionospheric(self):
		"""ionospheric commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_ionospheric'):
			from .Ionospheric import IonosphericCls
			self._ionospheric = IonosphericCls(self._core, self._cmd_group)
		return self._ionospheric

	@property
	def navic(self):
		"""navic commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Navic import NavicCls
			self._navic = NavicCls(self._core, self._cmd_group)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Qzss import QzssCls
			self._qzss = QzssCls(self._core, self._cmd_group)
		return self._qzss

	@property
	def tropospheric(self):
		"""tropospheric commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tropospheric'):
			from .Tropospheric import TroposphericCls
			self._tropospheric = TroposphericCls(self._core, self._cmd_group)
		return self._tropospheric

	def clone(self) -> 'AtmosphericCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AtmosphericCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
