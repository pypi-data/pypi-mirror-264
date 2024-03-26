from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EutraCls:
	"""Eutra commands group definition. 1281 total commands, 19 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eutra", core, parent)

	@property
	def bbfs(self):
		"""bbfs commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_bbfs'):
			from .Bbfs import BbfsCls
			self._bbfs = BbfsCls(self._core, self._cmd_group)
		return self._bbfs

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Clipping import ClippingCls
			self._clipping = ClippingCls(self._core, self._cmd_group)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def downlink(self):
		"""downlink commands group. 25 Sub-classes, 14 commands."""
		if not hasattr(self, '_downlink'):
			from .Downlink import DownlinkCls
			self._downlink = DownlinkCls(self._core, self._cmd_group)
		return self._downlink

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def logGen(self):
		"""logGen commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_logGen'):
			from .LogGen import LogGenCls
			self._logGen = LogGenCls(self._core, self._cmd_group)
		return self._logGen

	@property
	def notch(self):
		"""notch commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_notch'):
			from .Notch import NotchCls
			self._notch = NotchCls(self._core, self._cmd_group)
		return self._notch

	@property
	def powc(self):
		"""powc commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_powc'):
			from .Powc import PowcCls
			self._powc = PowcCls(self._core, self._cmd_group)
		return self._powc

	@property
	def setting(self):
		"""setting commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def tcw(self):
		"""tcw commands group. 12 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcw'):
			from .Tcw import TcwCls
			self._tcw = TcwCls(self._core, self._cmd_group)
		return self._tcw

	@property
	def tdd(self):
		"""tdd commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_tdd'):
			from .Tdd import TddCls
			self._tdd = TddCls(self._core, self._cmd_group)
		return self._tdd

	@property
	def tdw(self):
		"""tdw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tdw'):
			from .Tdw import TdwCls
			self._tdw = TdwCls(self._core, self._cmd_group)
		return self._tdw

	@property
	def timc(self):
		"""timc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_timc'):
			from .Timc import TimcCls
			self._timc = TimcCls(self._core, self._cmd_group)
		return self._timc

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def udt(self):
		"""udt commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_udt'):
			from .Udt import UdtCls
			self._udt = UdtCls(self._core, self._cmd_group)
		return self._udt

	@property
	def uplink(self):
		"""uplink commands group. 15 Sub-classes, 13 commands."""
		if not hasattr(self, '_uplink'):
			from .Uplink import UplinkCls
			self._uplink = UplinkCls(self._core, self._cmd_group)
		return self._uplink

	@property
	def uplane(self):
		"""uplane commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uplane'):
			from .Uplane import UplaneCls
			self._uplane = UplaneCls(self._core, self._cmd_group)
		return self._uplane

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Waveform import WaveformCls
			self._waveform = WaveformCls(self._core, self._cmd_group)
		return self._waveform

	# noinspection PyTypeChecker
	def get_duplexing(self) -> enums.EutraDuplexMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DUPLexing \n
		Snippet: value: enums.EutraDuplexMode = driver.source.bb.eutra.get_duplexing() \n
		Sets the duplexing mode. \n
			:return: duplexing: TDD| FDD
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DUPLexing?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexMode)

	def set_duplexing(self, duplexing: enums.EutraDuplexMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DUPLexing \n
		Snippet: driver.source.bb.eutra.set_duplexing(duplexing = enums.EutraDuplexMode.FDD) \n
		Sets the duplexing mode. \n
			:param duplexing: TDD| FDD
		"""
		param = Conversions.enum_scalar_to_str(duplexing, enums.EutraDuplexMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DUPLexing {param}')

	# noinspection PyTypeChecker
	def get_link(self) -> enums.UpDownDirection:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LINK \n
		Snippet: value: enums.UpDownDirection = driver.source.bb.eutra.get_link() \n
		Sets the transmission direction. \n
			:return: link: UP| DOWN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.UpDownDirection)

	def set_link(self, link: enums.UpDownDirection) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:LINK \n
		Snippet: driver.source.bb.eutra.set_link(link = enums.UpDownDirection.DOWN) \n
		Sets the transmission direction. \n
			:param link: UP| DOWN
		"""
		param = Conversions.enum_scalar_to_str(link, enums.UpDownDirection)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LINK {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:PRESet \n
		Snippet: driver.source.bb.eutra.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:EUTRa:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:PRESet \n
		Snippet: driver.source.bb.eutra.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:EUTRa:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:PRESet', opc_timeout_ms)

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:SLENgth \n
		Snippet: value: int = driver.source.bb.eutra.get_slength() \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. The maximum number of frames is calculated as follows: Max. No. of Frames = Arbitrary
		waveform memory size/(sampling rate x 10 ms) . \n
			:return: slength: integer Range: 1 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:SLENgth \n
		Snippet: driver.source.bb.eutra.set_slength(slength = 1) \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. The maximum number of frames is calculated as follows: Max. No. of Frames = Arbitrary
		waveform memory size/(sampling rate x 10 ms) . \n
			:param slength: integer Range: 1 to dynamic
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SLENgth {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:STATe \n
		Snippet: value: bool = driver.source.bb.eutra.get_state() \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:STATe \n
		Snippet: driver.source.bb.eutra.set_state(state = False) \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:STATe {param}')

	# noinspection PyTypeChecker
	def get_std_mode(self) -> enums.EutraStdMode:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:STDMode \n
		Snippet: value: enums.EutraStdMode = driver.source.bb.eutra.get_std_mode() \n
		Sets the supported 3GPP standard. \n
			:return: standard_mode: LTE| IOT| LIOT LTE Standalone LTE mode. IoT-specific commands containing the keywords EMTC or NIOT are discarded. IOT Standalone IoT mode. The commands related to LTE-specific features like carrier aggregation or MBSFN are discarded. LIOT Mixed LTE and IoT configuration, for example for interoperability tests.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:STDMode?')
		return Conversions.str_to_scalar_enum(response, enums.EutraStdMode)

	def set_std_mode(self, standard_mode: enums.EutraStdMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:STDMode \n
		Snippet: driver.source.bb.eutra.set_std_mode(standard_mode = enums.EutraStdMode.IOT) \n
		Sets the supported 3GPP standard. \n
			:param standard_mode: LTE| IOT| LIOT LTE Standalone LTE mode. IoT-specific commands containing the keywords EMTC or NIOT are discarded. IOT Standalone IoT mode. The commands related to LTE-specific features like carrier aggregation or MBSFN are discarded. LIOT Mixed LTE and IoT configuration, for example for interoperability tests.
		"""
		param = Conversions.enum_scalar_to_str(standard_mode, enums.EutraStdMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:STDMode {param}')

	def get_suslen(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:SUSLen \n
		Snippet: value: int = driver.source.bb.eutra.get_suslen() \n
		Sets the sequence length of the signal in number of subframes. The signal is calculated in advance and output in the
		arbitrary waveform generator. \n
			:return: sub_len: integer Range: 1 to 1E5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SUSLen?')
		return Conversions.str_to_int(response)

	def set_suslen(self, sub_len: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:SUSLen \n
		Snippet: driver.source.bb.eutra.set_suslen(sub_len = 1) \n
		Sets the sequence length of the signal in number of subframes. The signal is calculated in advance and output in the
		arbitrary waveform generator. \n
			:param sub_len: integer Range: 1 to 1E5
		"""
		param = Conversions.decimal_value_to_str(sub_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SUSLen {param}')

	def get_version(self) -> str:
		"""SCPI: [SOURce]:BB:EUTRa:VERSion \n
		Snippet: value: str = driver.source.bb.eutra.get_version() \n
		Queries the version of the 3GPP standard underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce:BB:EUTRa:VERSion?')
		return trim_str_response(response)

	def clone(self) -> 'EutraCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EutraCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
