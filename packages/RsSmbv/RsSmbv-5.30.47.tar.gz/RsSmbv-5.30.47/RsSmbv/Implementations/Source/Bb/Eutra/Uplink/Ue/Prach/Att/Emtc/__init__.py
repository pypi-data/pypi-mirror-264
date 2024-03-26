from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EmtcCls:
	"""Emtc commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("emtc", core, parent)

	@property
	def celv(self):
		"""celv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_celv'):
			from .Celv import CelvCls
			self._celv = CelvCls(self._core, self._cmd_group)
		return self._celv

	@property
	def dt(self):
		"""dt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dt'):
			from .Dt import DtCls
			self._dt = DtCls(self._core, self._cmd_group)
		return self._dt

	@property
	def frIndex(self):
		"""frIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frIndex'):
			from .FrIndex import FrIndexCls
			self._frIndex = FrIndexCls(self._core, self._cmd_group)
		return self._frIndex

	@property
	def ncsConf(self):
		"""ncsConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncsConf'):
			from .NcsConf import NcsConfCls
			self._ncsConf = NcsConfCls(self._core, self._cmd_group)
		return self._ncsConf

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def rsequence(self):
		"""rsequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsequence'):
			from .Rsequence import RsequenceCls
			self._rsequence = RsequenceCls(self._core, self._cmd_group)
		return self._rsequence

	@property
	def sfStart(self):
		"""sfStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfStart'):
			from .SfStart import SfStartCls
			self._sfStart = SfStartCls(self._core, self._cmd_group)
		return self._sfStart

	@property
	def sindex(self):
		"""sindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sindex'):
			from .Sindex import SindexCls
			self._sindex = SindexCls(self._core, self._cmd_group)
		return self._sindex

	def clone(self) -> 'EmtcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EmtcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
