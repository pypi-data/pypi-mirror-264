from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrcCls:
	"""Frc commands group definition. 33 total commands, 17 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frc", core, parent)

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Crate import CrateCls
			self._crate = CrateCls(self._core, self._cmd_group)
		return self._crate

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def derror(self):
		"""derror commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_derror'):
			from .Derror import DerrorCls
			self._derror = DerrorCls(self._core, self._cmd_group)
		return self._derror

	@property
	def dtx(self):
		"""dtx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtx'):
			from .Dtx import DtxCls
			self._dtx = DtxCls(self._core, self._cmd_group)
		return self._dtx

	@property
	def harq(self):
		"""harq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def hprocesses(self):
		"""hprocesses commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hprocesses'):
			from .Hprocesses import HprocessesCls
			self._hprocesses = HprocessesCls(self._core, self._cmd_group)
		return self._hprocesses

	@property
	def mibRate(self):
		"""mibRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mibRate'):
			from .MibRate import MibRateCls
			self._mibRate = MibRateCls(self._core, self._cmd_group)
		return self._mibRate

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def orate(self):
		"""orate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_orate'):
			from .Orate import OrateCls
			self._orate = OrateCls(self._core, self._cmd_group)
		return self._orate

	@property
	def paybits(self):
		"""paybits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paybits'):
			from .Paybits import PaybitsCls
			self._paybits = PaybitsCls(self._core, self._cmd_group)
		return self._paybits

	@property
	def pcCodes(self):
		"""pcCodes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcCodes'):
			from .PcCodes import PcCodesCls
			self._pcCodes = PcCodesCls(self._core, self._cmd_group)
		return self._pcCodes

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tbs(self):
		"""tbs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbs'):
			from .Tbs import TbsCls
			self._tbs = TbsCls(self._core, self._cmd_group)
		return self._tbs

	@property
	def ttiBits(self):
		"""ttiBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiBits'):
			from .TtiBits import TtiBitsCls
			self._ttiBits = TtiBitsCls(self._core, self._cmd_group)
		return self._ttiBits

	@property
	def ttiedch(self):
		"""ttiedch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiedch'):
			from .Ttiedch import TtiedchCls
			self._ttiedch = TtiedchCls(self._core, self._cmd_group)
		return self._ttiedch

	@property
	def ueCategory(self):
		"""ueCategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueCategory'):
			from .UeCategory import UeCategoryCls
			self._ueCategory = UeCategoryCls(self._core, self._cmd_group)
		return self._ueCategory

	def clone(self) -> 'FrcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
