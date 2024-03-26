from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TerminalCls:
	"""Terminal commands group definition. 52 total commands, 15 Subgroups, 0 group commands
	Repeated Capability: Terminal, default value after init: Terminal.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("terminal", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_terminal_get', 'repcap_terminal_set', repcap.Terminal.Nr1)

	def repcap_terminal_set(self, terminal: repcap.Terminal) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Terminal.Default
		Default value after init: Terminal.Nr1"""
		self._cmd_group.set_repcap_enum_value(terminal)

	def repcap_terminal_get(self) -> repcap.Terminal:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def ackChannel(self):
		"""ackChannel commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_ackChannel'):
			from .AckChannel import AckChannelCls
			self._ackChannel = AckChannelCls(self._core, self._cmd_group)
		return self._ackChannel

	@property
	def acycle(self):
		"""acycle commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_acycle'):
			from .Acycle import AcycleCls
			self._acycle = AcycleCls(self._core, self._cmd_group)
		return self._acycle

	@property
	def apChannel(self):
		"""apChannel commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_apChannel'):
			from .ApChannel import ApChannelCls
			self._apChannel = ApChannelCls(self._core, self._cmd_group)
		return self._apChannel

	@property
	def dchannel(self):
		"""dchannel commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_dchannel'):
			from .Dchannel import DchannelCls
			self._dchannel = DchannelCls(self._core, self._cmd_group)
		return self._dchannel

	@property
	def dqSpreading(self):
		"""dqSpreading commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dqSpreading'):
			from .DqSpreading import DqSpreadingCls
			self._dqSpreading = DqSpreadingCls(self._core, self._cmd_group)
		return self._dqSpreading

	@property
	def drcChannel(self):
		"""drcChannel commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_drcChannel'):
			from .DrcChannel import DrcChannelCls
			self._drcChannel = DrcChannelCls(self._core, self._cmd_group)
		return self._drcChannel

	@property
	def dscChannel(self):
		"""dscChannel commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dscChannel'):
			from .DscChannel import DscChannelCls
			self._dscChannel = DscChannelCls(self._core, self._cmd_group)
		return self._dscChannel

	@property
	def imask(self):
		"""imask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imask'):
			from .Imask import ImaskCls
			self._imask = ImaskCls(self._core, self._cmd_group)
		return self._imask

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def pchannel(self):
		"""pchannel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pchannel'):
			from .Pchannel import PchannelCls
			self._pchannel = PchannelCls(self._core, self._cmd_group)
		return self._pchannel

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plength'):
			from .Plength import PlengthCls
			self._plength = PlengthCls(self._core, self._cmd_group)
		return self._plength

	@property
	def qmask(self):
		"""qmask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qmask'):
			from .Qmask import QmaskCls
			self._qmask = QmaskCls(self._core, self._cmd_group)
		return self._qmask

	@property
	def rriChannel(self):
		"""rriChannel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rriChannel'):
			from .RriChannel import RriChannelCls
			self._rriChannel = RriChannelCls(self._core, self._cmd_group)
		return self._rriChannel

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def subType(self):
		"""subType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subType'):
			from .SubType import SubTypeCls
			self._subType = SubTypeCls(self._core, self._cmd_group)
		return self._subType

	def clone(self) -> 'TerminalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TerminalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
