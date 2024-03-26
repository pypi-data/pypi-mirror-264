from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoffsetCls:
	"""Coffset commands group definition. 31 total commands, 13 Subgroups, 0 group commands
	Repeated Capability: Offset, default value after init: Offset.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coffset", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_offset_get', 'repcap_offset_set', repcap.Offset.Nr1)

	def repcap_offset_set(self, offset: repcap.Offset) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Offset.Default
		Default value after init: Offset.Nr1"""
		self._cmd_group.set_repcap_enum_value(offset)

	def repcap_offset_get(self) -> repcap.Offset:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def ccoding(self):
		"""ccoding commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Ccoding import CcodingCls
			self._ccoding = CcodingCls(self._core, self._cmd_group)
		return self._ccoding

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 1 commands."""
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
	def flength(self):
		"""flength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_flength'):
			from .Flength import FlengthCls
			self._flength = FlengthCls(self._core, self._cmd_group)
		return self._flength

	@property
	def lcMask(self):
		"""lcMask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lcMask'):
			from .LcMask import LcMaskCls
			self._lcMask = LcMaskCls(self._core, self._cmd_group)
		return self._lcMask

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def qwCode(self):
		"""qwCode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qwCode'):
			from .QwCode import QwCodeCls
			self._qwCode = QwCodeCls(self._core, self._cmd_group)
		return self._qwCode

	@property
	def realtime(self):
		"""realtime commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_realtime'):
			from .Realtime import RealtimeCls
			self._realtime = RealtimeCls(self._core, self._cmd_group)
		return self._realtime

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tpc(self):
		"""tpc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Tpc import TpcCls
			self._tpc = TpcCls(self._core, self._cmd_group)
		return self._tpc

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def wcode(self):
		"""wcode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wcode'):
			from .Wcode import WcodeCls
			self._wcode = WcodeCls(self._core, self._cmd_group)
		return self._wcode

	@property
	def wlength(self):
		"""wlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wlength'):
			from .Wlength import WlengthCls
			self._wlength = WlengthCls(self._core, self._cmd_group)
		return self._wlength

	def clone(self) -> 'CoffsetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CoffsetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
