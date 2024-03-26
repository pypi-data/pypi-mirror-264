from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HsetCls:
	"""Hset commands group definition. 37 total commands, 29 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hset", core, parent)

	@property
	def acLength(self):
		"""acLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acLength'):
			from .AcLength import AcLengthCls
			self._acLength = AcLengthCls(self._core, self._cmd_group)
		return self._acLength

	@property
	def altModulation(self):
		"""altModulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_altModulation'):
			from .AltModulation import AltModulationCls
			self._altModulation = AltModulationCls(self._core, self._cmd_group)
		return self._altModulation

	@property
	def amode(self):
		"""amode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amode'):
			from .Amode import AmodeCls
			self._amode = AmodeCls(self._core, self._cmd_group)
		return self._amode

	@property
	def bcbtti(self):
		"""bcbtti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bcbtti'):
			from .Bcbtti import BcbttiCls
			self._bcbtti = BcbttiCls(self._core, self._cmd_group)
		return self._bcbtti

	@property
	def bpayload(self):
		"""bpayload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpayload'):
			from .Bpayload import BpayloadCls
			self._bpayload = BpayloadCls(self._core, self._cmd_group)
		return self._bpayload

	@property
	def clength(self):
		"""clength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_clength'):
			from .Clength import ClengthCls
			self._clength = ClengthCls(self._core, self._cmd_group)
		return self._clength

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Crate import CrateCls
			self._crate = CrateCls(self._core, self._cmd_group)
		return self._crate

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def harq(self):
		"""harq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def hscCode(self):
		"""hscCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hscCode'):
			from .HscCode import HscCodeCls
			self._hscCode = HscCodeCls(self._core, self._cmd_group)
		return self._hscCode

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def naiBitrate(self):
		"""naiBitrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naiBitrate'):
			from .NaiBitrate import NaiBitrateCls
			self._naiBitrate = NaiBitrateCls(self._core, self._cmd_group)
		return self._naiBitrate

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	@property
	def pwPattern(self):
		"""pwPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pwPattern'):
			from .PwPattern import PwPatternCls
			self._pwPattern = PwPatternCls(self._core, self._cmd_group)
		return self._pwPattern

	@property
	def rvpSequence(self):
		"""rvpSequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvpSequence'):
			from .RvpSequence import RvpSequenceCls
			self._rvpSequence = RvpSequenceCls(self._core, self._cmd_group)
		return self._rvpSequence

	@property
	def rvParameter(self):
		"""rvParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvParameter'):
			from .RvParameter import RvParameterCls
			self._rvParameter = RvParameterCls(self._core, self._cmd_group)
		return self._rvParameter

	@property
	def rvState(self):
		"""rvState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvState'):
			from .RvState import RvStateCls
			self._rvState = RvStateCls(self._core, self._cmd_group)
		return self._rvState

	@property
	def s64Qam(self):
		"""s64Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_s64Qam'):
			from .S64Qam import S64QamCls
			self._s64Qam = S64QamCls(self._core, self._cmd_group)
		return self._s64Qam

	@property
	def scCode(self):
		"""scCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scCode'):
			from .ScCode import ScCodeCls
			self._scCode = ScCodeCls(self._core, self._cmd_group)
		return self._scCode

	@property
	def seed(self):
		"""seed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seed'):
			from .Seed import SeedCls
			self._seed = SeedCls(self._core, self._cmd_group)
		return self._seed

	@property
	def slength(self):
		"""slength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Slength import SlengthCls
			self._slength = SlengthCls(self._core, self._cmd_group)
		return self._slength

	@property
	def spattern(self):
		"""spattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spattern'):
			from .Spattern import SpatternCls
			self._spattern = SpatternCls(self._core, self._cmd_group)
		return self._spattern

	@property
	def staPattern(self):
		"""staPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_staPattern'):
			from .StaPattern import StaPatternCls
			self._staPattern = StaPatternCls(self._core, self._cmd_group)
		return self._staPattern

	@property
	def tbs(self):
		"""tbs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbs'):
			from .Tbs import TbsCls
			self._tbs = TbsCls(self._core, self._cmd_group)
		return self._tbs

	@property
	def tpower(self):
		"""tpower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpower'):
			from .Tpower import TpowerCls
			self._tpower = TpowerCls(self._core, self._cmd_group)
		return self._tpower

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def ueCategory(self):
		"""ueCategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueCategory'):
			from .UeCategory import UeCategoryCls
			self._ueCategory = UeCategoryCls(self._core, self._cmd_group)
		return self._ueCategory

	@property
	def ueId(self):
		"""ueId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueId'):
			from .UeId import UeIdCls
			self._ueId = UeIdCls(self._core, self._cmd_group)
		return self._ueId

	@property
	def vibSize(self):
		"""vibSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vibSize'):
			from .VibSize import VibSizeCls
			self._vibSize = VibSizeCls(self._core, self._cmd_group)
		return self._vibSize

	def set(self, hset: int, baseStation=repcap.BaseStation.Default, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH0>:HSDPa:HSET \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.set(hset = 1, baseStation = repcap.BaseStation.Default, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param hset: No help available
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
		"""
		param = Conversions.decimal_value_to_str(hset)
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel{channelNull_cmd_val}:HSDPa:HSET {param}')

	def get(self, baseStation=repcap.BaseStation.Default, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH0>:HSDPa:HSET \n
		Snippet: value: int = driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.get(baseStation = repcap.BaseStation.Default, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: hset: No help available"""
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel{channelNull_cmd_val}:HSDPa:HSET?')
		return Conversions.str_to_int(response)

	def preset(self, baseStation=repcap.BaseStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:HSDPa:HSET:PRESet \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.preset(baseStation = repcap.BaseStation.Default) \n
		Sets the default settings of the channel table for the HSDPA H-Set mode. Channels 12 to 17 are preset for HSDPA H-Set 1. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
		"""
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel:HSDPa:HSET:PRESet')

	def preset_with_opc(self, baseStation=repcap.BaseStation.Default, opc_timeout_ms: int = -1) -> None:
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:HSDPa:HSET:PRESet \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.hsdpa.hset.preset_with_opc(baseStation = repcap.BaseStation.Default) \n
		Sets the default settings of the channel table for the HSDPA H-Set mode. Channels 12 to 17 are preset for HSDPA H-Set 1. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel:HSDPa:HSET:PRESet', opc_timeout_ms)

	def clone(self) -> 'HsetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HsetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
