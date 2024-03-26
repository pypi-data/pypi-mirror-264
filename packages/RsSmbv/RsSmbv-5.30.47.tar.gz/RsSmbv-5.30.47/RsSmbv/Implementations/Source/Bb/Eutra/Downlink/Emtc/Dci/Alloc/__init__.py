from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllocCls:
	"""Alloc commands group definition. 42 total commands, 42 Subgroups, 0 group commands
	Repeated Capability: AllocationNull, default value after init: AllocationNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alloc", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_allocationNull_get', 'repcap_allocationNull_set', repcap.AllocationNull.Nr0)

	def repcap_allocationNull_set(self, allocationNull: repcap.AllocationNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AllocationNull.Default
		Default value after init: AllocationNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(allocationNull)

	def repcap_allocationNull_get(self) -> repcap.AllocationNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def apsi(self):
		"""apsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apsi'):
			from .Apsi import ApsiCls
			self._apsi = ApsiCls(self._core, self._cmd_group)
		return self._apsi

	@property
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Bits import BitsCls
			self._bits = BitsCls(self._core, self._cmd_group)
		return self._bits

	@property
	def cces(self):
		"""cces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cces'):
			from .Cces import CcesCls
			self._cces = CcesCls(self._core, self._cmd_group)
		return self._cces

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def csiRequest(self):
		"""csiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiRequest'):
			from .CsiRequest import CsiRequestCls
			self._csiRequest = CsiRequestCls(self._core, self._cmd_group)
		return self._csiRequest

	@property
	def daIndex(self):
		"""daIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_daIndex'):
			from .DaIndex import DaIndexCls
			self._daIndex = DaIndexCls(self._core, self._cmd_group)
		return self._daIndex

	@property
	def diInfo(self):
		"""diInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_diInfo'):
			from .DiInfo import DiInfoCls
			self._diInfo = DiInfoCls(self._core, self._cmd_group)
		return self._diInfo

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Fmt import FmtCls
			self._fmt = FmtCls(self._core, self._cmd_group)
		return self._fmt

	@property
	def harq(self):
		"""harq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def hresOffset(self):
		"""hresOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hresOffset'):
			from .HresOffset import HresOffsetCls
			self._hresOffset = HresOffsetCls(self._core, self._cmd_group)
		return self._hresOffset

	@property
	def idcce(self):
		"""idcce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_idcce'):
			from .Idcce import IdcceCls
			self._idcce = IdcceCls(self._core, self._cmd_group)
		return self._idcce

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Mcs import McsCls
			self._mcs = McsCls(self._core, self._cmd_group)
		return self._mcs

	@property
	def mpdcchset(self):
		"""mpdcchset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mpdcchset'):
			from .Mpdcchset import MpdcchsetCls
			self._mpdcchset = MpdcchsetCls(self._core, self._cmd_group)
		return self._mpdcchset

	@property
	def ndcces(self):
		"""ndcces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndcces'):
			from .Ndcces import NdccesCls
			self._ndcces = NdccesCls(self._core, self._cmd_group)
		return self._ndcces

	@property
	def ndind(self):
		"""ndind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndind'):
			from .Ndind import NdindCls
			self._ndind = NdindCls(self._core, self._cmd_group)
		return self._ndind

	@property
	def nrep(self):
		"""nrep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrep'):
			from .Nrep import NrepCls
			self._nrep = NrepCls(self._core, self._cmd_group)
		return self._nrep

	@property
	def pagng(self):
		"""pagng commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pagng'):
			from .Pagng import PagngCls
			self._pagng = PagngCls(self._core, self._cmd_group)
		return self._pagng

	@property
	def pdcch(self):
		"""pdcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdcch'):
			from .Pdcch import PdcchCls
			self._pdcch = PdcchCls(self._core, self._cmd_group)
		return self._pdcch

	@property
	def pdsHopping(self):
		"""pdsHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdsHopping'):
			from .PdsHopping import PdsHoppingCls
			self._pdsHopping = PdsHoppingCls(self._core, self._cmd_group)
		return self._pdsHopping

	@property
	def pfrHopp(self):
		"""pfrHopp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfrHopp'):
			from .PfrHopp import PfrHoppCls
			self._pfrHopp = PfrHoppCls(self._core, self._cmd_group)
		return self._pfrHopp

	@property
	def pmiConfirm(self):
		"""pmiConfirm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmiConfirm'):
			from .PmiConfirm import PmiConfirmCls
			self._pmiConfirm = PmiConfirmCls(self._core, self._cmd_group)
		return self._pmiConfirm

	@property
	def praMask(self):
		"""praMask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_praMask'):
			from .PraMask import PraMaskCls
			self._praMask = PraMaskCls(self._core, self._cmd_group)
		return self._praMask

	@property
	def praPreamble(self):
		"""praPreamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_praPreamble'):
			from .PraPreamble import PraPreambleCls
			self._praPreamble = PraPreambleCls(self._core, self._cmd_group)
		return self._praPreamble

	@property
	def praStart(self):
		"""praStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_praStart'):
			from .PraStart import PraStartCls
			self._praStart = PraStartCls(self._core, self._cmd_group)
		return self._praStart

	@property
	def rba(self):
		"""rba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rba'):
			from .Rba import RbaCls
			self._rba = RbaCls(self._core, self._cmd_group)
		return self._rba

	@property
	def rbaf(self):
		"""rbaf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbaf'):
			from .Rbaf import RbafCls
			self._rbaf = RbafCls(self._core, self._cmd_group)
		return self._rbaf

	@property
	def repmpdcch(self):
		"""repmpdcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repmpdcch'):
			from .Repmpdcch import RepmpdcchCls
			self._repmpdcch = RepmpdcchCls(self._core, self._cmd_group)
		return self._repmpdcch

	@property
	def reppdsch(self):
		"""reppdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reppdsch'):
			from .Reppdsch import ReppdschCls
			self._reppdsch = ReppdschCls(self._core, self._cmd_group)
		return self._reppdsch

	@property
	def rver(self):
		"""rver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rver'):
			from .Rver import RverCls
			self._rver = RverCls(self._core, self._cmd_group)
		return self._rver

	@property
	def sfrNumber(self):
		"""sfrNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfrNumber'):
			from .SfrNumber import SfrNumberCls
			self._sfrNumber = SfrNumberCls(self._core, self._cmd_group)
		return self._sfrNumber

	@property
	def srsRequest(self):
		"""srsRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsRequest'):
			from .SrsRequest import SrsRequestCls
			self._srsRequest = SrsRequestCls(self._core, self._cmd_group)
		return self._srsRequest

	@property
	def ssp(self):
		"""ssp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssp'):
			from .Ssp import SspCls
			self._ssp = SspCls(self._core, self._cmd_group)
		return self._ssp

	@property
	def strv(self):
		"""strv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_strv'):
			from .Strv import StrvCls
			self._strv = StrvCls(self._core, self._cmd_group)
		return self._strv

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .StsFrame import StsFrameCls
			self._stsFrame = StsFrameCls(self._core, self._cmd_group)
		return self._stsFrame

	@property
	def tbs(self):
		"""tbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbs'):
			from .Tbs import TbsCls
			self._tbs = TbsCls(self._core, self._cmd_group)
		return self._tbs

	@property
	def tcmd(self):
		"""tcmd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcmd'):
			from .Tcmd import TcmdCls
			self._tcmd = TcmdCls(self._core, self._cmd_group)
		return self._tcmd

	@property
	def tpcPusch(self):
		"""tpcPusch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcPusch'):
			from .TpcPusch import TpcPuschCls
			self._tpcPusch = TpcPuschCls(self._core, self._cmd_group)
		return self._tpcPusch

	@property
	def tpmprec(self):
		"""tpmprec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpmprec'):
			from .Tpmprec import TpmprecCls
			self._tpmprec = TpmprecCls(self._core, self._cmd_group)
		return self._tpmprec

	@property
	def ueId(self):
		"""ueId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueId'):
			from .UeId import UeIdCls
			self._ueId = UeIdCls(self._core, self._cmd_group)
		return self._ueId

	@property
	def ueMode(self):
		"""ueMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueMode'):
			from .UeMode import UeModeCls
			self._ueMode = UeModeCls(self._core, self._cmd_group)
		return self._ueMode

	@property
	def ulIndex(self):
		"""ulIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulIndex'):
			from .UlIndex import UlIndexCls
			self._ulIndex = UlIndexCls(self._core, self._cmd_group)
		return self._ulIndex

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'AllocCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AllocCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
