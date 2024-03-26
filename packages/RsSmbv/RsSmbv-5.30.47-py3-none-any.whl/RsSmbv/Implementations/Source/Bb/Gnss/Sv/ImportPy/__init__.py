from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImportPyCls:
	"""ImportPy commands group definition. 42 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("importPy", core, parent)

	@property
	def beidou(self):
		"""beidou commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_beidou'):
			from .Beidou import BeidouCls
			self._beidou = BeidouCls(self._core, self._cmd_group)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_glonass'):
			from .Glonass import GlonassCls
			self._glonass = GlonassCls(self._core, self._cmd_group)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_gps'):
			from .Gps import GpsCls
			self._gps = GpsCls(self._core, self._cmd_group)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_navic'):
			from .Navic import NavicCls
			self._navic = NavicCls(self._core, self._cmd_group)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_qzss'):
			from .Qzss import QzssCls
			self._qzss = QzssCls(self._core, self._cmd_group)
		return self._qzss

	@property
	def sbas(self):
		"""sbas commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .Sbas import SbasCls
			self._sbas = SbasCls(self._core, self._cmd_group)
		return self._sbas

	def clone(self) -> 'ImportPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ImportPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
