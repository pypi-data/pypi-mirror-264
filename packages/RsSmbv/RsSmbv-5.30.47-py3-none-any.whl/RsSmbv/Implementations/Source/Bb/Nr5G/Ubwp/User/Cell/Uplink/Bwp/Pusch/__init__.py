from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschCls:
	"""Pusch commands group definition. 81 total commands, 33 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pusch", core, parent)

	@property
	def a02List(self):
		"""a02List commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_a02List'):
			from .A02List import A02ListCls
			self._a02List = A02ListCls(self._core, self._cmd_group)
		return self._a02List

	@property
	def accList(self):
		"""accList commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_accList'):
			from .AccList import AccListCls
			self._accList = AccListCls(self._core, self._cmd_group)
		return self._accList

	@property
	def apPresent(self):
		"""apPresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apPresent'):
			from .ApPresent import ApPresentCls
			self._apPresent = ApPresentCls(self._core, self._cmd_group)
		return self._apPresent

	@property
	def bharq(self):
		"""bharq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bharq'):
			from .Bharq import BharqCls
			self._bharq = BharqCls(self._core, self._cmd_group)
		return self._bharq

	@property
	def brv(self):
		"""brv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_brv'):
			from .Brv import BrvCls
			self._brv = BrvCls(self._core, self._cmd_group)
		return self._brv

	@property
	def cbSubset(self):
		"""cbSubset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbSubset'):
			from .CbSubset import CbSubsetCls
			self._cbSubset = CbSubsetCls(self._core, self._cmd_group)
		return self._cbSubset

	@property
	def dmta(self):
		"""dmta commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmta'):
			from .Dmta import DmtaCls
			self._dmta = DmtaCls(self._core, self._cmd_group)
		return self._dmta

	@property
	def dmtb(self):
		"""dmtb commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmtb'):
			from .Dmtb import DmtbCls
			self._dmtb = DmtbCls(self._core, self._cmd_group)
		return self._dmtb

	@property
	def dsid(self):
		"""dsid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsid'):
			from .Dsid import DsidCls
			self._dsid = DsidCls(self._core, self._cmd_group)
		return self._dsid

	@property
	def dsInit(self):
		"""dsInit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsInit'):
			from .DsInit import DsInitCls
			self._dsInit = DsInitCls(self._core, self._cmd_group)
		return self._dsInit

	@property
	def fhOffsets(self):
		"""fhOffsets commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fhOffsets'):
			from .FhOffsets import FhOffsetsCls
			self._fhOffsets = FhOffsetsCls(self._core, self._cmd_group)
		return self._fhOffsets

	@property
	def fhop(self):
		"""fhop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fhop'):
			from .Fhop import FhopCls
			self._fhop = FhopCls(self._core, self._cmd_group)
		return self._fhop

	@property
	def fptr(self):
		"""fptr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fptr'):
			from .Fptr import FptrCls
			self._fptr = FptrCls(self._core, self._cmd_group)
		return self._fptr

	@property
	def hp5Bits(self):
		"""hp5Bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hp5Bits'):
			from .Hp5Bits import Hp5BitsCls
			self._hp5Bits = Hp5BitsCls(self._core, self._cmd_group)
		return self._hp5Bits

	@property
	def isin(self):
		"""isin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isin'):
			from .Isin import IsinCls
			self._isin = IsinCls(self._core, self._cmd_group)
		return self._isin

	@property
	def mcbGroups(self):
		"""mcbGroups commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcbGroups'):
			from .McbGroups import McbGroupsCls
			self._mcbGroups = McbGroupsCls(self._core, self._cmd_group)
		return self._mcbGroups

	@property
	def mcsTable(self):
		"""mcsTable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsTable'):
			from .McsTable import McsTableCls
			self._mcsTable = McsTableCls(self._core, self._cmd_group)
		return self._mcsTable

	@property
	def mrank(self):
		"""mrank commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mrank'):
			from .Mrank import MrankCls
			self._mrank = MrankCls(self._core, self._cmd_group)
		return self._mrank

	@property
	def mttPrecoding(self):
		"""mttPrecoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mttPrecoding'):
			from .MttPrecoding import MttPrecodingCls
			self._mttPrecoding = MttPrecodingCls(self._core, self._cmd_group)
		return self._mttPrecoding

	@property
	def oi01(self):
		"""oi01 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oi01'):
			from .Oi01 import Oi01Cls
			self._oi01 = Oi01Cls(self._core, self._cmd_group)
		return self._oi01

	@property
	def olpc(self):
		"""olpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_olpc'):
			from .Olpc import OlpcCls
			self._olpc = OlpcCls(self._core, self._cmd_group)
		return self._olpc

	@property
	def pi01(self):
		"""pi01 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pi01'):
			from .Pi01 import Pi01Cls
			self._pi01 = Pi01Cls(self._core, self._cmd_group)
		return self._pi01

	@property
	def pi02(self):
		"""pi02 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pi02'):
			from .Pi02 import Pi02Cls
			self._pi02 = Pi02Cls(self._core, self._cmd_group)
		return self._pi02

	@property
	def ppsl(self):
		"""ppsl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ppsl'):
			from .Ppsl import PpslCls
			self._ppsl = PpslCls(self._core, self._cmd_group)
		return self._ppsl

	@property
	def rbgSize(self):
		"""rbgSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbgSize'):
			from .RbgSize import RbgSizeCls
			self._rbgSize = RbgSizeCls(self._core, self._cmd_group)
		return self._rbgSize

	@property
	def resAlloc(self):
		"""resAlloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resAlloc'):
			from .ResAlloc import ResAllocCls
			self._resAlloc = ResAllocCls(self._core, self._cmd_group)
		return self._resAlloc

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Scrambling import ScramblingCls
			self._scrambling = ScramblingCls(self._core, self._cmd_group)
		return self._scrambling

	@property
	def t1Gran(self):
		"""t1Gran commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t1Gran'):
			from .T1Gran import T1GranCls
			self._t1Gran = T1GranCls(self._core, self._cmd_group)
		return self._t1Gran

	@property
	def tpState(self):
		"""tpState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpState'):
			from .TpState import TpStateCls
			self._tpState = TpStateCls(self._core, self._cmd_group)
		return self._tpState

	@property
	def txConfig(self):
		"""txConfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txConfig'):
			from .TxConfig import TxConfigCls
			self._txConfig = TxConfigCls(self._core, self._cmd_group)
		return self._txConfig

	@property
	def u2Tpc(self):
		"""u2Tpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_u2Tpc'):
			from .U2Tpc import U2TpcCls
			self._u2Tpc = U2TpcCls(self._core, self._cmd_group)
		return self._u2Tpc

	@property
	def uitl(self):
		"""uitl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uitl'):
			from .Uitl import UitlCls
			self._uitl = UitlCls(self._core, self._cmd_group)
		return self._uitl

	@property
	def xoverhead(self):
		"""xoverhead commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xoverhead'):
			from .Xoverhead import XoverheadCls
			self._xoverhead = XoverheadCls(self._core, self._cmd_group)
		return self._xoverhead

	def clone(self) -> 'PuschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PuschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
