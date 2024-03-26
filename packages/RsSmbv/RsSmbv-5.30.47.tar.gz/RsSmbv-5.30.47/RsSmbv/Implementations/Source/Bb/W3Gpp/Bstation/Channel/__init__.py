from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChannelCls:
	"""Channel commands group definition. 100 total commands, 14 Subgroups, 1 group commands
	Repeated Capability: ChannelNull, default value after init: ChannelNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("channel", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channelNull_get', 'repcap_channelNull_set', repcap.ChannelNull.Nr0)

	def repcap_channelNull_set(self, channelNull: repcap.ChannelNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ChannelNull.Default
		Default value after init: ChannelNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(channelNull)

	def repcap_channelNull_get(self) -> repcap.ChannelNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def aich(self):
		"""aich commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_aich'):
			from .Aich import AichCls
			self._aich = AichCls(self._core, self._cmd_group)
		return self._aich

	@property
	def apaich(self):
		"""apaich commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_apaich'):
			from .Apaich import ApaichCls
			self._apaich = ApaichCls(self._core, self._cmd_group)
		return self._apaich

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .Ccode import CcodeCls
			self._ccode = CcodeCls(self._core, self._cmd_group)
		return self._ccode

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dpcch(self):
		"""dpcch commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpcch'):
			from .Dpcch import DpcchCls
			self._dpcch = DpcchCls(self._core, self._cmd_group)
		return self._dpcch

	@property
	def fdpch(self):
		"""fdpch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdpch'):
			from .Fdpch import FdpchCls
			self._fdpch = FdpchCls(self._core, self._cmd_group)
		return self._fdpch

	@property
	def hsdpa(self):
		"""hsdpa commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsdpa'):
			from .Hsdpa import HsdpaCls
			self._hsdpa = HsdpaCls(self._core, self._cmd_group)
		return self._hsdpa

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Toffset import ToffsetCls
			self._toffset = ToffsetCls(self._core, self._cmd_group)
		return self._toffset

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def hsupa(self):
		"""hsupa commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsupa'):
			from .Hsupa import HsupaCls
			self._hsupa = HsupaCls(self._core, self._cmd_group)
		return self._hsupa

	def preset(self, baseStation=repcap.BaseStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:PRESet \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.preset(baseStation = repcap.BaseStation.Default) \n
		The command calls the default settings of the channel table. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
		"""
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel:PRESet')

	def preset_with_opc(self, baseStation=repcap.BaseStation.Default, opc_timeout_ms: int = -1) -> None:
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:PRESet \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.preset_with_opc(baseStation = repcap.BaseStation.Default) \n
		The command calls the default settings of the channel table. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel:PRESet', opc_timeout_ms)

	def clone(self) -> 'ChannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ChannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
