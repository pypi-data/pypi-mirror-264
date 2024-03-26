from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HsdpaCls:
	"""Hsdpa commands group definition. 18 total commands, 15 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hsdpa", core, parent)

	@property
	def bpayload(self):
		"""bpayload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpayload'):
			from .Bpayload import BpayloadCls
			self._bpayload = BpayloadCls(self._core, self._cmd_group)
		return self._bpayload

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Crate import CrateCls
			self._crate = CrateCls(self._core, self._cmd_group)
		return self._crate

	@property
	def ctsCount(self):
		"""ctsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctsCount'):
			from .CtsCount import CtsCountCls
			self._ctsCount = CtsCountCls(self._core, self._cmd_group)
		return self._ctsCount

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def harq(self):
		"""harq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def mibt(self):
		"""mibt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mibt'):
			from .Mibt import MibtCls
			self._mibt = MibtCls(self._core, self._cmd_group)
		return self._mibt

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def ncbTti(self):
		"""ncbTti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncbTti'):
			from .NcbTti import NcbTtiCls
			self._ncbTti = NcbTtiCls(self._core, self._cmd_group)
		return self._ncbTti

	@property
	def rvParameter(self):
		"""rvParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvParameter'):
			from .RvParameter import RvParameterCls
			self._rvParameter = RvParameterCls(self._core, self._cmd_group)
		return self._rvParameter

	@property
	def rvSequence(self):
		"""rvSequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvSequence'):
			from .RvSequence import RvSequenceCls
			self._rvSequence = RvSequenceCls(self._core, self._cmd_group)
		return self._rvSequence

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def tbs(self):
		"""tbs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbs'):
			from .Tbs import TbsCls
			self._tbs = TbsCls(self._core, self._cmd_group)
		return self._tbs

	@property
	def tsCount(self):
		"""tsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsCount'):
			from .TsCount import TsCountCls
			self._tsCount = TsCountCls(self._core, self._cmd_group)
		return self._tsCount

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .TtInterval import TtIntervalCls
			self._ttInterval = TtIntervalCls(self._core, self._cmd_group)
		return self._ttInterval

	@property
	def ueCategory(self):
		"""ueCategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueCategory'):
			from .UeCategory import UeCategoryCls
			self._ueCategory = UeCategoryCls(self._core, self._cmd_group)
		return self._ueCategory

	def clone(self) -> 'HsdpaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HsdpaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
