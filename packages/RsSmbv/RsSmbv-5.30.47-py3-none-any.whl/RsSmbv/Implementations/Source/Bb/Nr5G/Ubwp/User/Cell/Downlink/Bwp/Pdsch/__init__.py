from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PdschCls:
	"""Pdsch commands group definition. 73 total commands, 28 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdsch", core, parent)

	@property
	def ag12(self):
		"""ag12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ag12'):
			from .Ag12 import Ag12Cls
			self._ag12 = Ag12Cls(self._core, self._cmd_group)
		return self._ag12

	@property
	def ap12(self):
		"""ap12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ap12'):
			from .Ap12 import Ap12Cls
			self._ap12 = Ap12Cls(self._core, self._cmd_group)
		return self._ap12

	@property
	def cbgf(self):
		"""cbgf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cbgf'):
			from .Cbgf import CbgfCls
			self._cbgf = CbgfCls(self._core, self._cmd_group)
		return self._cbgf

	@property
	def di12(self):
		"""di12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di12'):
			from .Di12 import Di12Cls
			self._di12 = Di12Cls(self._core, self._cmd_group)
		return self._di12

	@property
	def dmta(self):
		"""dmta commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmta'):
			from .Dmta import DmtaCls
			self._dmta = DmtaCls(self._core, self._cmd_group)
		return self._dmta

	@property
	def dmtb(self):
		"""dmtb commands group. 7 Sub-classes, 0 commands."""
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
	def ha12(self):
		"""ha12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ha12'):
			from .Ha12 import Ha12Cls
			self._ha12 = Ha12Cls(self._core, self._cmd_group)
		return self._ha12

	@property
	def hp5Bits(self):
		"""hp5Bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hp5Bits'):
			from .Hp5Bits import Hp5BitsCls
			self._hp5Bits = Hp5BitsCls(self._core, self._cmd_group)
		return self._hp5Bits

	@property
	def lselected(self):
		"""lselected commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lselected'):
			from .Lselected import LselectedCls
			self._lselected = LselectedCls(self._core, self._cmd_group)
		return self._lselected

	@property
	def maOffset(self):
		"""maOffset commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_maOffset'):
			from .MaOffset import MaOffsetCls
			self._maOffset = MaOffsetCls(self._core, self._cmd_group)
		return self._maOffset

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
	def mcwdci(self):
		"""mcwdci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcwdci'):
			from .Mcwdci import McwdciCls
			self._mcwdci = McwdciCls(self._core, self._cmd_group)
		return self._mcwdci

	@property
	def pi11(self):
		"""pi11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pi11'):
			from .Pi11 import Pi11Cls
			self._pi11 = Pi11Cls(self._core, self._cmd_group)
		return self._pi11

	@property
	def pi12(self):
		"""pi12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pi12'):
			from .Pi12 import Pi12Cls
			self._pi12 = Pi12Cls(self._core, self._cmd_group)
		return self._pi12

	@property
	def prec(self):
		"""prec commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_prec'):
			from .Prec import PrecCls
			self._prec = PrecCls(self._core, self._cmd_group)
		return self._prec

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
	def rv12(self):
		"""rv12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rv12'):
			from .Rv12 import Rv12Cls
			self._rv12 = Rv12Cls(self._core, self._cmd_group)
		return self._rv12

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Scrambling import ScramblingCls
			self._scrambling = ScramblingCls(self._core, self._cmd_group)
		return self._scrambling

	@property
	def tci(self):
		"""tci commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tci'):
			from .Tci import TciCls
			self._tci = TciCls(self._core, self._cmd_group)
		return self._tci

	@property
	def td(self):
		"""td commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_td'):
			from .Td import TdCls
			self._td = TdCls(self._core, self._cmd_group)
		return self._td

	@property
	def tdaLists(self):
		"""tdaLists commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdaLists'):
			from .TdaLists import TdaListsCls
			self._tdaLists = TdaListsCls(self._core, self._cmd_group)
		return self._tdaLists

	@property
	def tdaNum(self):
		"""tdaNum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdaNum'):
			from .TdaNum import TdaNumCls
			self._tdaNum = TdaNumCls(self._core, self._cmd_group)
		return self._tdaNum

	@property
	def tdml(self):
		"""tdml commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdml'):
			from .Tdml import TdmlCls
			self._tdml = TdmlCls(self._core, self._cmd_group)
		return self._tdml

	@property
	def vpInter(self):
		"""vpInter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vpInter'):
			from .VpInter import VpInterCls
			self._vpInter = VpInterCls(self._core, self._cmd_group)
		return self._vpInter

	@property
	def xoverhead(self):
		"""xoverhead commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xoverhead'):
			from .Xoverhead import XoverheadCls
			self._xoverhead = XoverheadCls(self._core, self._cmd_group)
		return self._xoverhead

	def clone(self) -> 'PdschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PdschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
