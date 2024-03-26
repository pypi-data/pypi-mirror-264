from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DciConfCls:
	"""DciConf commands group definition. 42 total commands, 37 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dciConf", core, parent)

	@property
	def apLayer(self):
		"""apLayer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apLayer'):
			from .ApLayer import ApLayerCls
			self._apLayer = ApLayerCls(self._core, self._cmd_group)
		return self._apLayer

	@property
	def bitData(self):
		"""bitData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitData'):
			from .BitData import BitDataCls
			self._bitData = BitDataCls(self._core, self._cmd_group)
		return self._bitData

	@property
	def ciField(self):
		"""ciField commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ciField'):
			from .CiField import CiFieldCls
			self._ciField = CiFieldCls(self._core, self._cmd_group)
		return self._ciField

	@property
	def cqiRequest(self):
		"""cqiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cqiRequest'):
			from .CqiRequest import CqiRequestCls
			self._cqiRequest = CqiRequestCls(self._core, self._cmd_group)
		return self._cqiRequest

	@property
	def csDmrs(self):
		"""csDmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csDmrs'):
			from .CsDmrs import CsDmrsCls
			self._csDmrs = CsDmrsCls(self._core, self._cmd_group)
		return self._csDmrs

	@property
	def csiRequest(self):
		"""csiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiRequest'):
			from .CsiRequest import CsiRequestCls
			self._csiRequest = CsiRequestCls(self._core, self._cmd_group)
		return self._csiRequest

	@property
	def dlaIndex(self):
		"""dlaIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlaIndex'):
			from .DlaIndex import DlaIndexCls
			self._dlaIndex = DlaIndexCls(self._core, self._cmd_group)
		return self._dlaIndex

	@property
	def dpOffset(self):
		"""dpOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpOffset'):
			from .DpOffset import DpOffsetCls
			self._dpOffset = DpOffsetCls(self._core, self._cmd_group)
		return self._dpOffset

	@property
	def f1Amode(self):
		"""f1Amode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f1Amode'):
			from .F1Amode import F1AmodeCls
			self._f1Amode = F1AmodeCls(self._core, self._cmd_group)
		return self._f1Amode

	@property
	def gap(self):
		"""gap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gap'):
			from .Gap import GapCls
			self._gap = GapCls(self._core, self._cmd_group)
		return self._gap

	@property
	def hack(self):
		"""hack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hack'):
			from .Hack import HackCls
			self._hack = HackCls(self._core, self._cmd_group)
		return self._hack

	@property
	def hpn(self):
		"""hpn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hpn'):
			from .Hpn import HpnCls
			self._hpn = HpnCls(self._core, self._cmd_group)
		return self._hpn

	@property
	def laaSubframe(self):
		"""laaSubframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_laaSubframe'):
			from .LaaSubframe import LaaSubframeCls
			self._laaSubframe = LaaSubframeCls(self._core, self._cmd_group)
		return self._laaSubframe

	@property
	def mcsr(self):
		"""mcsr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsr'):
			from .Mcsr import McsrCls
			self._mcsr = McsrCls(self._core, self._cmd_group)
		return self._mcsr

	@property
	def ndi(self):
		"""ndi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndi'):
			from .Ndi import NdiCls
			self._ndi = NdiCls(self._core, self._cmd_group)
		return self._ndi

	@property
	def pdre(self):
		"""pdre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdre'):
			from .Pdre import PdreCls
			self._pdre = PdreCls(self._core, self._cmd_group)
		return self._pdre

	@property
	def pfHopping(self):
		"""pfHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfHopping'):
			from .PfHopping import PfHoppingCls
			self._pfHopping = PfHoppingCls(self._core, self._cmd_group)
		return self._pfHopping

	@property
	def pmi(self):
		"""pmi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmi'):
			from .Pmi import PmiCls
			self._pmi = PmiCls(self._core, self._cmd_group)
		return self._pmi

	@property
	def prach(self):
		"""prach commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_prach'):
			from .Prach import PrachCls
			self._prach = PrachCls(self._core, self._cmd_group)
		return self._prach

	@property
	def precInfo(self):
		"""precInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_precInfo'):
			from .PrecInfo import PrecInfoCls
			self._precInfo = PrecInfoCls(self._core, self._cmd_group)
		return self._precInfo

	@property
	def rah(self):
		"""rah commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rah'):
			from .Rah import RahCls
			self._rah = RahCls(self._core, self._cmd_group)
		return self._rah

	@property
	def rahr(self):
		"""rahr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rahr'):
			from .Rahr import RahrCls
			self._rahr = RahrCls(self._core, self._cmd_group)
		return self._rahr

	@property
	def raType(self):
		"""raType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_raType'):
			from .RaType import RaTypeCls
			self._raType = RaTypeCls(self._core, self._cmd_group)
		return self._raType

	@property
	def rba(self):
		"""rba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rba'):
			from .Rba import RbaCls
			self._rba = RbaCls(self._core, self._cmd_group)
		return self._rba

	@property
	def rv(self):
		"""rv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rv'):
			from .Rv import RvCls
			self._rv = RvCls(self._core, self._cmd_group)
		return self._rv

	@property
	def sid(self):
		"""sid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sid'):
			from .Sid import SidCls
			self._sid = SidCls(self._core, self._cmd_group)
		return self._sid

	@property
	def srsRequest(self):
		"""srsRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsRequest'):
			from .SrsRequest import SrsRequestCls
			self._srsRequest = SrsRequestCls(self._core, self._cmd_group)
		return self._srsRequest

	@property
	def swapFlag(self):
		"""swapFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swapFlag'):
			from .SwapFlag import SwapFlagCls
			self._swapFlag = SwapFlagCls(self._core, self._cmd_group)
		return self._swapFlag

	@property
	def tb1(self):
		"""tb1 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb1'):
			from .Tb1 import Tb1Cls
			self._tb1 = Tb1Cls(self._core, self._cmd_group)
		return self._tb1

	@property
	def tb2(self):
		"""tb2 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb2'):
			from .Tb2 import Tb2Cls
			self._tb2 = Tb2Cls(self._core, self._cmd_group)
		return self._tb2

	@property
	def tbsi(self):
		"""tbsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbsi'):
			from .Tbsi import TbsiCls
			self._tbsi = TbsiCls(self._core, self._cmd_group)
		return self._tbsi

	@property
	def tpcc(self):
		"""tpcc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcc'):
			from .Tpcc import TpccCls
			self._tpcc = TpccCls(self._core, self._cmd_group)
		return self._tpcc

	@property
	def tpcInstr(self):
		"""tpcInstr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcInstr'):
			from .TpcInstr import TpcInstrCls
			self._tpcInstr = TpcInstrCls(self._core, self._cmd_group)
		return self._tpcInstr

	@property
	def tpmi(self):
		"""tpmi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpmi'):
			from .Tpmi import TpmiCls
			self._tpmi = TpmiCls(self._core, self._cmd_group)
		return self._tpmi

	@property
	def ulDlConf(self):
		"""ulDlConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulDlConf'):
			from .UlDlConf import UlDlConfCls
			self._ulDlConf = UlDlConfCls(self._core, self._cmd_group)
		return self._ulDlConf

	@property
	def ulIndex(self):
		"""ulIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulIndex'):
			from .UlIndex import UlIndexCls
			self._ulIndex = UlIndexCls(self._core, self._cmd_group)
		return self._ulIndex

	@property
	def vrba(self):
		"""vrba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vrba'):
			from .Vrba import VrbaCls
			self._vrba = VrbaCls(self._core, self._cmd_group)
		return self._vrba

	def clone(self) -> 'DciConfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DciConfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
