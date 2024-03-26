from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 438 total commands, 12 Subgroups, 0 group commands
	Repeated Capability: UserNull, default value after init: UserNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_userNull_get', 'repcap_userNull_set', repcap.UserNull.Nr0)

	def repcap_userNull_set(self, userNull: repcap.UserNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserNull.Default
		Default value after init: UserNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(userNull)

	def repcap_userNull_get(self) -> repcap.UserNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cell(self):
		"""cell commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	@property
	def dsch(self):
		"""dsch commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_dsch'):
			from .Dsch import DschCls
			self._dsch = DschCls(self._core, self._cmd_group)
		return self._dsch

	@property
	def dspc(self):
		"""dspc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dspc'):
			from .Dspc import DspcCls
			self._dspc = DspcCls(self._core, self._cmd_group)
		return self._dspc

	@property
	def ncarrier(self):
		"""ncarrier commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncarrier'):
			from .Ncarrier import NcarrierCls
			self._ncarrier = NcarrierCls(self._core, self._cmd_group)
		return self._ncarrier

	@property
	def numSfi(self):
		"""numSfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_numSfi'):
			from .NumSfi import NumSfiCls
			self._numSfi = NumSfiCls(self._core, self._cmd_group)
		return self._numSfi

	@property
	def oran(self):
		"""oran commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_oran'):
			from .Oran import OranCls
			self._oran = OranCls(self._core, self._cmd_group)
		return self._oran

	@property
	def pupload(self):
		"""pupload commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_pupload'):
			from .Pupload import PuploadCls
			self._pupload = PuploadCls(self._core, self._cmd_group)
		return self._pupload

	@property
	def puuci(self):
		"""puuci commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_puuci'):
			from .Puuci import PuuciCls
			self._puuci = PuuciCls(self._core, self._cmd_group)
		return self._puuci

	@property
	def rnti(self):
		"""rnti commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_rnti'):
			from .Rnti import RntiCls
			self._rnti = RntiCls(self._core, self._cmd_group)
		return self._rnti

	@property
	def ssch(self):
		"""ssch commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_ssch'):
			from .Ssch import SschCls
			self._ssch = SschCls(self._core, self._cmd_group)
		return self._ssch

	@property
	def ueId(self):
		"""ueId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueId'):
			from .UeId import UeIdCls
			self._ueId = UeIdCls(self._core, self._cmd_group)
		return self._ueId

	@property
	def usch(self):
		"""usch commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_usch'):
			from .Usch import UschCls
			self._usch = UschCls(self._core, self._cmd_group)
		return self._usch

	def clone(self) -> 'UserCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UserCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
