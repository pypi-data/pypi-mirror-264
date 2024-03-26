from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CellCls:
	"""Cell commands group definition. 12 total commands, 12 Subgroups, 0 group commands
	Repeated Capability: CellNull, default value after init: CellNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cell", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_cellNull_get', 'repcap_cellNull_set', repcap.CellNull.Nr0)

	def repcap_cellNull_set(self, cellNull: repcap.CellNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CellNull.Default
		Default value after init: CellNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(cellNull)

	def repcap_cellNull_get(self) -> repcap.CellNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Bw import BwCls
			self._bw = BwCls(self._core, self._cmd_group)
		return self._bw

	@property
	def csrs(self):
		"""csrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csrs'):
			from .Csrs import CsrsCls
			self._csrs = CsrsCls(self._core, self._cmd_group)
		return self._csrs

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Dfreq import DfreqCls
			self._dfreq = DfreqCls(self._core, self._cmd_group)
		return self._dfreq

	@property
	def dmrs(self):
		"""dmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmrs'):
			from .Dmrs import DmrsCls
			self._dmrs = DmrsCls(self._core, self._cmd_group)
		return self._dmrs

	@property
	def duplexing(self):
		"""duplexing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duplexing'):
			from .Duplexing import DuplexingCls
			self._duplexing = DuplexingCls(self._core, self._cmd_group)
		return self._duplexing

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Index import IndexCls
			self._index = IndexCls(self._core, self._cmd_group)
		return self._index

	@property
	def spsConf(self):
		"""spsConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spsConf'):
			from .SpsConf import SpsConfCls
			self._spsConf = SpsConfCls(self._core, self._cmd_group)
		return self._spsConf

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def suConfiguration(self):
		"""suConfiguration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_suConfiguration'):
			from .SuConfiguration import SuConfigurationCls
			self._suConfiguration = SuConfigurationCls(self._core, self._cmd_group)
		return self._suConfiguration

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Tdelay import TdelayCls
			self._tdelay = TdelayCls(self._core, self._cmd_group)
		return self._tdelay

	@property
	def udConf(self):
		"""udConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_udConf'):
			from .UdConf import UdConfCls
			self._udConf = UdConfCls(self._core, self._cmd_group)
		return self._udConf

	def clone(self) -> 'CellCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CellCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
