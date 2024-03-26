from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CinfoCls:
	"""Cinfo commands group definition. 20 total commands, 20 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cinfo", core, parent)

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Bw import BwCls
			self._bw = BwCls(self._core, self._cmd_group)
		return self._bw

	@property
	def cindication(self):
		"""cindication commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cindication'):
			from .Cindication import CindicationCls
			self._cindication = CindicationCls(self._core, self._cmd_group)
		return self._cindication

	@property
	def csRequired(self):
		"""csRequired commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csRequired'):
			from .CsRequired import CsRequiredCls
			self._csRequired = CsRequiredCls(self._core, self._cmd_group)
		return self._csRequired

	@property
	def doppler(self):
		"""doppler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_doppler'):
			from .Doppler import DopplerCls
			self._doppler = DopplerCls(self._core, self._cmd_group)
		return self._doppler

	@property
	def ereserved(self):
		"""ereserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ereserved'):
			from .Ereserved import EreservedCls
			self._ereserved = EreservedCls(self._core, self._cmd_group)
		return self._ereserved

	@property
	def giltf(self):
		"""giltf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_giltf'):
			from .Giltf import GiltfCls
			self._giltf = GiltfCls(self._core, self._cmd_group)
		return self._giltf

	@property
	def heeht(self):
		"""heeht commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_heeht'):
			from .Heeht import HeehtCls
			self._heeht = HeehtCls(self._core, self._cmd_group)
		return self._heeht

	@property
	def hreserved(self):
		"""hreserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hreserved'):
			from .Hreserved import HreservedCls
			self._hreserved = HreservedCls(self._core, self._cmd_group)
		return self._hreserved

	@property
	def len(self):
		"""len commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_len'):
			from .Len import LenCls
			self._len = LenCls(self._core, self._cmd_group)
		return self._len

	@property
	def lesSeg(self):
		"""lesSeg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lesSeg'):
			from .LesSeg import LesSegCls
			self._lesSeg = LesSegCls(self._core, self._cmd_group)
		return self._lesSeg

	@property
	def mltfMode(self):
		"""mltfMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mltfMode'):
			from .MltfMode import MltfModeCls
			self._mltfMode = MltfModeCls(self._core, self._cmd_group)
		return self._mltfMode

	@property
	def nhlSym(self):
		"""nhlSym commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nhlSym'):
			from .NhlSym import NhlSymCls
			self._nhlSym = NhlSymCls(self._core, self._cmd_group)
		return self._nhlSym

	@property
	def pextension(self):
		"""pextension commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pextension'):
			from .Pextension import PextensionCls
			self._pextension = PextensionCls(self._core, self._cmd_group)
		return self._pextension

	@property
	def rsv(self):
		"""rsv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsv'):
			from .Rsv import RsvCls
			self._rsv = RsvCls(self._core, self._cmd_group)
		return self._rsv

	@property
	def spareUse(self):
		"""spareUse commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spareUse'):
			from .SpareUse import SpareUseCls
			self._spareUse = SpareUseCls(self._core, self._cmd_group)
		return self._spareUse

	@property
	def stbc(self):
		"""stbc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stbc'):
			from .Stbc import StbcCls
			self._stbc = StbcCls(self._core, self._cmd_group)
		return self._stbc

	@property
	def suiPresent(self):
		"""suiPresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_suiPresent'):
			from .SuiPresent import SuiPresentCls
			self._suiPresent = SuiPresentCls(self._core, self._cmd_group)
		return self._suiPresent

	@property
	def tfType(self):
		"""tfType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfType'):
			from .TfType import TfTypeCls
			self._tfType = TfTypeCls(self._core, self._cmd_group)
		return self._tfType

	@property
	def ttype(self):
		"""ttype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttype'):
			from .Ttype import TtypeCls
			self._ttype = TtypeCls(self._core, self._cmd_group)
		return self._ttype

	@property
	def txpow(self):
		"""txpow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txpow'):
			from .Txpow import TxpowCls
			self._txpow = TxpowCls(self._core, self._cmd_group)
		return self._txpow

	def clone(self) -> 'CinfoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CinfoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
