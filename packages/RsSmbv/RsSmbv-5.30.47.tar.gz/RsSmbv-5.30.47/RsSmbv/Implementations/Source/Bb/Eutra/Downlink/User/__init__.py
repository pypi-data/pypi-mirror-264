from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 105 total commands, 26 Subgroups, 0 group commands
	Repeated Capability: UserIx, default value after init: UserIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_userIx_get', 'repcap_userIx_set', repcap.UserIx.Nr1)

	def repcap_userIx_set(self, userIx: repcap.UserIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserIx.Default
		Default value after init: UserIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(userIx)

	def repcap_userIx_get(self) -> repcap.UserIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def apm(self):
		"""apm commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_apm'):
			from .Apm import ApmCls
			self._apm = ApmCls(self._core, self._cmd_group)
		return self._apm

	@property
	def asPy(self):
		"""asPy commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_asPy'):
			from .AsPy import AsPyCls
			self._asPy = AsPyCls(self._core, self._cmd_group)
		return self._asPy

	@property
	def asrs(self):
		"""asrs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_asrs'):
			from .Asrs import AsrsCls
			self._asrs = AsrsCls(self._core, self._cmd_group)
		return self._asrs

	@property
	def ca(self):
		"""ca commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ca'):
			from .Ca import CaCls
			self._ca = CaCls(self._core, self._cmd_group)
		return self._ca

	@property
	def caw(self):
		"""caw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_caw'):
			from .Caw import CawCls
			self._caw = CawCls(self._core, self._cmd_group)
		return self._caw

	@property
	def ccoding(self):
		"""ccoding commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Ccoding import CcodingCls
			self._ccoding = CcodingCls(self._core, self._cmd_group)
		return self._ccoding

	@property
	def cell(self):
		"""cell commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Dselect import DselectCls
			self._dselect = DselectCls(self._core, self._cmd_group)
		return self._dselect

	@property
	def eimtaRnti(self):
		"""eimtaRnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eimtaRnti'):
			from .EimtaRnti import EimtaRntiCls
			self._eimtaRnti = EimtaRntiCls(self._core, self._cmd_group)
		return self._eimtaRnti

	@property
	def epdcch(self):
		"""epdcch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_epdcch'):
			from .Epdcch import EpdcchCls
			self._epdcch = EpdcchCls(self._core, self._cmd_group)
		return self._epdcch

	@property
	def initPattern(self):
		"""initPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_initPattern'):
			from .InitPattern import InitPatternCls
			self._initPattern = InitPatternCls(self._core, self._cmd_group)
		return self._initPattern

	@property
	def mcsTwo(self):
		"""mcsTwo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mcsTwo'):
			from .McsTwo import McsTwoCls
			self._mcsTwo = McsTwoCls(self._core, self._cmd_group)
		return self._mcsTwo

	@property
	def niot(self):
		"""niot commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_niot'):
			from .Niot import NiotCls
			self._niot = NiotCls(self._core, self._cmd_group)
		return self._niot

	@property
	def pa(self):
		"""pa commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pa'):
			from .Pa import PaCls
			self._pa = PaCls(self._core, self._cmd_group)
		return self._pa

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def release(self):
		"""release commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_release'):
			from .Release import ReleaseCls
			self._release = ReleaseCls(self._core, self._cmd_group)
		return self._release

	@property
	def scrambling(self):
		"""scrambling commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Scrambling import ScramblingCls
			self._scrambling = ScramblingCls(self._core, self._cmd_group)
		return self._scrambling

	@property
	def sps(self):
		"""sps commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_sps'):
			from .Sps import SpsCls
			self._sps = SpsCls(self._core, self._cmd_group)
		return self._sps

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def sthp(self):
		"""sthp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sthp'):
			from .Sthp import SthpCls
			self._sthp = SthpCls(self._core, self._cmd_group)
		return self._sthp

	@property
	def taltIndex(self):
		"""taltIndex commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_taltIndex'):
			from .TaltIndex import TaltIndexCls
			self._taltIndex = TaltIndexCls(self._core, self._cmd_group)
		return self._taltIndex

	@property
	def txm(self):
		"""txm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txm'):
			from .Txm import TxmCls
			self._txm = TxmCls(self._core, self._cmd_group)
		return self._txm

	@property
	def uec(self):
		"""uec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uec'):
			from .Uec import UecCls
			self._uec = UecCls(self._core, self._cmd_group)
		return self._uec

	@property
	def ueId(self):
		"""ueId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueId'):
			from .UeId import UeIdCls
			self._ueId = UeIdCls(self._core, self._cmd_group)
		return self._ueId

	@property
	def ulca(self):
		"""ulca commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ulca'):
			from .Ulca import UlcaCls
			self._ulca = UlcaCls(self._core, self._cmd_group)
		return self._ulca

	def clone(self) -> 'UserCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UserCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
