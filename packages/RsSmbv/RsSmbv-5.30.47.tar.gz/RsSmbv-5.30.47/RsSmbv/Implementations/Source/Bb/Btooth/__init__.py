from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BtoothCls:
	"""Btooth commands group definition. 380 total commands, 21 Subgroups, 18 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("btooth", core, parent)

	@property
	def ccrc(self):
		"""ccrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccrc'):
			from .Ccrc import CcrcCls
			self._ccrc = CcrcCls(self._core, self._cmd_group)
		return self._ccrc

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Clipping import ClippingCls
			self._clipping = ClippingCls(self._core, self._cmd_group)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def cs(self):
		"""cs commands group. 9 Sub-classes, 13 commands."""
		if not hasattr(self, '_cs'):
			from .Cs import CsCls
			self._cs = CsCls(self._core, self._cmd_group)
		return self._cs

	@property
	def dtTest(self):
		"""dtTest commands group. 3 Sub-classes, 7 commands."""
		if not hasattr(self, '_dtTest'):
			from .DtTest import DtTestCls
			self._dtTest = DtTestCls(self._core, self._cmd_group)
		return self._dtTest

	@property
	def econfig(self):
		"""econfig commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_econfig'):
			from .Econfig import EconfigCls
			self._econfig = EconfigCls(self._core, self._cmd_group)
		return self._econfig

	@property
	def econfiguration(self):
		"""econfiguration commands group. 4 Sub-classes, 11 commands."""
		if not hasattr(self, '_econfiguration'):
			from .Econfiguration import EconfigurationCls
			self._econfiguration = EconfigurationCls(self._core, self._cmd_group)
		return self._econfiguration

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def hdr(self):
		"""hdr commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_hdr'):
			from .Hdr import HdrCls
			self._hdr = HdrCls(self._core, self._cmd_group)
		return self._hdr

	@property
	def hr(self):
		"""hr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hr'):
			from .Hr import HrCls
			self._hr = HrCls(self._core, self._cmd_group)
		return self._hr

	@property
	def mhdt(self):
		"""mhdt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mhdt'):
			from .Mhdt import MhdtCls
			self._mhdt = MhdtCls(self._core, self._cmd_group)
		return self._mhdt

	@property
	def msettings(self):
		"""msettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_msettings'):
			from .Msettings import MsettingsCls
			self._msettings = MsettingsCls(self._core, self._cmd_group)
		return self._msettings

	@property
	def pconfiguration(self):
		"""pconfiguration commands group. 6 Sub-classes, 15 commands."""
		if not hasattr(self, '_pconfiguration'):
			from .Pconfiguration import PconfigurationCls
			self._pconfiguration = PconfigurationCls(self._core, self._cmd_group)
		return self._pconfiguration

	@property
	def phymacCfg(self):
		"""phymacCfg commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_phymacCfg'):
			from .PhymacCfg import PhymacCfgCls
			self._phymacCfg = PhymacCfgCls(self._core, self._cmd_group)
		return self._phymacCfg

	@property
	def pramping(self):
		"""pramping commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_pramping'):
			from .Pramping import PrampingCls
			self._pramping = PrampingCls(self._core, self._cmd_group)
		return self._pramping

	@property
	def qhs(self):
		"""qhs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qhs'):
			from .Qhs import QhsCls
			self._qhs = QhsCls(self._core, self._cmd_group)
		return self._qhs

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def unit(self):
		"""unit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unit'):
			from .Unit import UnitCls
			self._unit = UnitCls(self._core, self._cmd_group)
		return self._unit

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Waveform import WaveformCls
			self._waveform = WaveformCls(self._core, self._cmd_group)
		return self._waveform

	# noinspection PyTypeChecker
	def get_bc_role(self) -> enums.BtoCtrlRol:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:BCRole \n
		Snippet: value: enums.BtoCtrlRol = driver.source.bb.btooth.get_bc_role() \n
		Determines the controller role. Depending on the selected channel type different roles are assigned to the controller.
		For channel type 'Data', Central or Peripheral can be assigned. If channel type 'Advertising' is selected, the parameter
		is read only and displayed directly above the graph. \n
			:return: bc_role: CENTral| PERipheral| ADVertiser| SCANner| INITiator CENTral Selects Central as controller role. PERipheral Selects Peripheral as controller role. ADVertiser|SCANner|INITiator Assigned roles depending on the selected packet type of the respective channel type.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:BCRole?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCtrlRol)

	def set_bc_role(self, bc_role: enums.BtoCtrlRol) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:BCRole \n
		Snippet: driver.source.bb.btooth.set_bc_role(bc_role = enums.BtoCtrlRol.ADVertiser) \n
		Determines the controller role. Depending on the selected channel type different roles are assigned to the controller.
		For channel type 'Data', Central or Peripheral can be assigned. If channel type 'Advertising' is selected, the parameter
		is read only and displayed directly above the graph. \n
			:param bc_role: CENTral| PERipheral| ADVertiser| SCANner| INITiator CENTral Selects Central as controller role. PERipheral Selects Peripheral as controller role. ADVertiser|SCANner|INITiator Assigned roles depending on the selected packet type of the respective channel type.
		"""
		param = Conversions.enum_scalar_to_str(bc_role, enums.BtoCtrlRol)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:BCRole {param}')

	def get_bc_text(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:BCText \n
		Snippet: value: str = driver.source.bb.btooth.get_bc_text() \n
		Queries the state and controller role. \n
			:return: bc_text: string Connected (only data channel type) Advertiser (only advertising channel type) ADV_IND, ADV_DIRECT_IND, ADV_NONCONN_IND, ADV_SCAN_IND Within R&S SMBVB-K117 also ADV_EXT_IND, AUX_ADV_IND, AUX_SYNC_IND, AUX_CHAIN_IND Scanner (only advertising channel type) SCAN_REQ, SCAN_RSP Within R&S SMBVB-K117 also AUX_SCAN_REQ, AUX_SCAN_RSP Initiator (only advertising channel type) CONNECT_IND Within R&S SMBVB-K117 also AUX_CONNECT_REQ, AUX_CONNECT_RSP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:BCText?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_bmode(self) -> enums.BtoMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:BMODe \n
		Snippet: value: enums.BtoMode = driver.source.bb.btooth.get_bmode() \n
		Determines the Bluetooth mode. \n
			:return: bmode: BASic| BLENergy BASic Selects Bluetooth mode BR + EDR. BLENergy Selects Bluetooth LE.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:BMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoMode)

	def set_bmode(self, bmode: enums.BtoMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:BMODe \n
		Snippet: driver.source.bb.btooth.set_bmode(bmode = enums.BtoMode.BASic) \n
		Determines the Bluetooth mode. \n
			:param bmode: BASic| BLENergy BASic Selects Bluetooth mode BR + EDR. BLENergy Selects Bluetooth LE.
		"""
		param = Conversions.enum_scalar_to_str(bmode, enums.BtoMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:BMODe {param}')

	# noinspection PyTypeChecker
	def get_ctype(self) -> enums.BtoChnnelType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CTYPe \n
		Snippet: value: enums.BtoChnnelType = driver.source.bb.btooth.get_ctype() \n
		Determines the channel type. Advertising and data are available. \n
			:return: ctype: ADVertising| DATA ADVertising Selects channel type advertising. DATA Selects channel type data. Devices in a connected state transmit data channel packets in connection events with a start point and an interval.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoChnnelType)

	def set_ctype(self, ctype: enums.BtoChnnelType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CTYPe \n
		Snippet: driver.source.bb.btooth.set_ctype(ctype = enums.BtoChnnelType.ADVertising) \n
		Determines the channel type. Advertising and data are available. \n
			:param ctype: ADVertising| DATA ADVertising Selects channel type advertising. DATA Selects channel type data. Devices in a connected state transmit data channel packets in connection events with a start point and an interval.
		"""
		param = Conversions.enum_scalar_to_str(ctype, enums.BtoChnnelType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CTYPe {param}')

	# noinspection PyTypeChecker
	def get_dcycle(self) -> enums.LowHigh:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:DCYCle \n
		Snippet: value: enums.LowHigh = driver.source.bb.btooth.get_dcycle() \n
		Specifies duty cycle for directed advertising (packet type ADV_DIRECT_IND) . \n
			:return: dcycle: LOW| HIGH
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DCYCle?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_dcycle(self, dcycle: enums.LowHigh) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:DCYCle \n
		Snippet: driver.source.bb.btooth.set_dcycle(dcycle = enums.LowHigh.HIGH) \n
		Specifies duty cycle for directed advertising (packet type ADV_DIRECT_IND) . \n
			:param dcycle: LOW| HIGH
		"""
		param = Conversions.enum_scalar_to_str(dcycle, enums.LowHigh)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DCYCle {param}')

	def get_duration(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:DURation \n
		Snippet: value: float = driver.source.bb.btooth.get_duration() \n
		Specifies the transmission duration of CONTINUOUS payload transmission. Command sets the values in ms. Query returns
		values in s. \n
			:return: duration: float Range: depending on modulation format, symbols per a bit and payload type , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DURation?')
		return Conversions.str_to_float(response)

	def set_duration(self, duration: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:DURation \n
		Snippet: driver.source.bb.btooth.set_duration(duration = 1.0) \n
		Specifies the transmission duration of CONTINUOUS payload transmission. Command sets the values in ms. Query returns
		values in s. \n
			:param duration: float Range: depending on modulation format, symbols per a bit and payload type , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DURation {param}')

	# noinspection PyTypeChecker
	def get_hdrp_phy(self) -> enums.BtoHdrpPhy:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:HDRPphy \n
		Snippet: value: enums.BtoHdrpPhy = driver.source.bb.btooth.get_hdrp_phy() \n
		No command help available \n
			:return: hdrp_phy: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:HDRPphy?')
		return Conversions.str_to_scalar_enum(response, enums.BtoHdrpPhy)

	def set_hdrp_phy(self, hdrp_phy: enums.BtoHdrpPhy) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:HDRPphy \n
		Snippet: driver.source.bb.btooth.set_hdrp_phy(hdrp_phy = enums.BtoHdrpPhy.HDRP4) \n
		No command help available \n
			:param hdrp_phy: No help available
		"""
		param = Conversions.enum_scalar_to_str(hdrp_phy, enums.BtoHdrpPhy)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:HDRPphy {param}')

	# noinspection PyTypeChecker
	def get_mformat(self) -> enums.PackFormat:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:MFORmat \n
		Snippet: value: enums.PackFormat = driver.source.bb.btooth.get_mformat() \n
		Specifies the physical layer used for CONTINUOUS payload transmission. \n
			:return: mod_fmt: L1M| L2M| LCOD L1M: LE 1M L2M: LE 2M LCOD: LE coded
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:MFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.PackFormat)

	def set_mformat(self, mod_fmt: enums.PackFormat) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:MFORmat \n
		Snippet: driver.source.bb.btooth.set_mformat(mod_fmt = enums.PackFormat.L1M) \n
		Specifies the physical layer used for CONTINUOUS payload transmission. \n
			:param mod_fmt: L1M| L2M| LCOD L1M: LE 1M L2M: LE 2M LCOD: LE coded
		"""
		param = Conversions.enum_scalar_to_str(mod_fmt, enums.PackFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:MFORmat {param}')

	# noinspection PyTypeChecker
	def get_pformat(self) -> enums.BtoPackFormat:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PFORmat \n
		Snippet: value: enums.BtoPackFormat = driver.source.bb.btooth.get_pformat() \n
		Specifies the physical layer of LE signal. \n
			:return: pformat: L1M| L2M| LCOD L1M LE 1M L2M LE 2M LCOD LE coded
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.BtoPackFormat)

	def set_pformat(self, pformat: enums.BtoPackFormat) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PFORmat \n
		Snippet: driver.source.bb.btooth.set_pformat(pformat = enums.BtoPackFormat.BLE4M) \n
		Specifies the physical layer of LE signal. \n
			:param pformat: L1M| L2M| LCOD L1M LE 1M L2M LE 2M LCOD LE coded
		"""
		param = Conversions.enum_scalar_to_str(pformat, enums.BtoPackFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PFORmat {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PRESet \n
		Snippet: driver.source.bb.btooth.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:BTOoth:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PRESet \n
		Snippet: driver.source.bb.btooth.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:BTOoth:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:BTOoth:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_ptype(self) -> enums.BtoPckType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PTYPe \n
		Snippet: value: enums.BtoPckType = driver.source.bb.btooth.get_ptype() \n
		The available packets depend on the selected transport mode. All packet types as defined in the Bluetooth specifications
		are supported. \n
			:return: ptype: ID| NULL| POLL| FHS| DM1| DH1| DM3| DH3| DM5| DH5| AUX1| ADH1| ADH3| ADH5| AEDH1| AEDH3| AEDH5| HV1| HV2| HV3| DV| EV3| EV4| EV5| EEV3| EEV5| EEEV3| EEEV5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoPckType)

	def set_ptype(self, ptype: enums.BtoPckType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PTYPe \n
		Snippet: driver.source.bb.btooth.set_ptype(ptype = enums.BtoPckType.ADH1) \n
		The available packets depend on the selected transport mode. All packet types as defined in the Bluetooth specifications
		are supported. \n
			:param ptype: ID| NULL| POLL| FHS| DM1| DH1| DM3| DH3| DM5| DH5| AUX1| ADH1| ADH3| ADH5| AEDH1| AEDH3| AEDH5| HV1| HV2| HV3| DV| EV3| EV4| EV5| EEV3| EEV5| EEEV3| EEEV5
		"""
		param = Conversions.enum_scalar_to_str(ptype, enums.BtoPckType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PTYPe {param}')

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:SLENgth \n
		Snippet: value: int = driver.source.bb.btooth.get_slength() \n
		Sets the sequence length of the Bluetooth signal in number of frames. This signal is calculated in advance and output in
		the arbitrary waveform generator. \n
			:return: slength: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:SLENgth \n
		Snippet: driver.source.bb.btooth.set_slength(slength = 1) \n
		Sets the sequence length of the Bluetooth signal in number of frames. This signal is calculated in advance and output in
		the arbitrary waveform generator. \n
			:param slength: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:SLENgth {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:STATe \n
		Snippet: value: bool = driver.source.bb.btooth.get_state() \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:STATe \n
		Snippet: driver.source.bb.btooth.set_state(state = False) \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:STATe {param}')

	# noinspection PyTypeChecker
	def get_stiming(self) -> enums.BtoSlotTiming:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:STIMing \n
		Snippet: value: enums.BtoSlotTiming = driver.source.bb.btooth.get_stiming() \n
		Selects the Rx slot timing mode. \n
			:return: slot_timing: TX| LOOPback
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:STIMing?')
		return Conversions.str_to_scalar_enum(response, enums.BtoSlotTiming)

	def set_stiming(self, slot_timing: enums.BtoSlotTiming) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:STIMing \n
		Snippet: driver.source.bb.btooth.set_stiming(slot_timing = enums.BtoSlotTiming.LOOPback) \n
		Selects the Rx slot timing mode. \n
			:param slot_timing: TX| LOOPback
		"""
		param = Conversions.enum_scalar_to_str(slot_timing, enums.BtoSlotTiming)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:STIMing {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.BtoTranMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TMODe \n
		Snippet: value: enums.BtoTranMode = driver.source.bb.btooth.get_tmode() \n
		Selects the transport mode. \n
			:return: tmode: ACL| SCO| ESCO ACL Asynchronous connection-less mode used for a point-to-point multipoint link between a Central and all Peripherals. SCO Synchronous connection-oriented mode used for a point-to-point link between a Central and a specific Peripheral. ESCO Enhanced synchronous connection-oriented mode used for a symmetric or asymmetric point-to point link between a Central and a specific Peripheral.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoTranMode)

	def set_tmode(self, tmode: enums.BtoTranMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TMODe \n
		Snippet: driver.source.bb.btooth.set_tmode(tmode = enums.BtoTranMode.ACL) \n
		Selects the transport mode. \n
			:param tmode: ACL| SCO| ESCO ACL Asynchronous connection-less mode used for a point-to-point multipoint link between a Central and all Peripherals. SCO Synchronous connection-oriented mode used for a point-to-point link between a Central and a specific Peripheral. ESCO Enhanced synchronous connection-oriented mode used for a symmetric or asymmetric point-to point link between a Central and a specific Peripheral.
		"""
		param = Conversions.enum_scalar_to_str(tmode, enums.BtoTranMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TMODe {param}')

	# noinspection PyTypeChecker
	def get_up_type(self) -> enums.BtoUlpPckType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:UPTYpe \n
		Snippet: value: enums.BtoUlpPckType = driver.source.bb.btooth.get_up_type() \n
		Selects the packet type. The available packets depend on the selected channel type and installed options. The tables
		below provide an overview. For more information, see data sheet. R&S SMBVB-K60 packet/PDU types
			Table Header: <UpType> / Packet/PDU type \n
			- AIND ADINd ANINd SREQ SRSP CREQ ADCind DATA CUReq CMReq TIND EREQ / ADV_IND ADV_DIRECT_IND ADV_NONCONN_IND SCAN_REQ SCAN_RSP CONNECT_IND ADV_SCAN_IND DATA LL_CONNECTION_UPDATE_IND LL_CHANNEL_MAP_IND LL_TERMINATE_IND LL_ENC_REQ
			- ERSP SEReq SERSp URSP FREQ FRSP TPACket PEReq PERSp VIND RIND / LL_ENC_RSP LL_START_ENC_REQ LL_START_ENC_RSP LL_UNKNONW_RSP LL_FEATURE_REQ LL_FEATURE_RSP TEST PACKET LL_PAUSE_ENC_REQ LL_PAUSE_ENC_RSP LL_VERSION_IND LL_REJECT_IND
		R&S SMBVB-K117 packet/PDU types
			Table Header: <UpType> / Packet/PDU type \n
			- PREQ PRSP PUIN LRSP SFR CPR CPRS REIN PIR PIRS AEINd AAINd ACINd / LL_PHY_REQ LL_PHY_RSP LL_PHY_UPDATE_IND LL_LENGTH_RSP LL_PERIPHERAL_FEATURE_REQ LL_CONNECTION_PARAM_REQ LL_CONNECTION_PARAM_RSP LL_REJECT_EXT_IND LL_PING_REQ LL_PING_RSP ADV_EXT_IND AUX_ADV_IND AUX_CHAIN_IND
			- ASINd ASReq ASPSp ACRSp ACReq MUCH CONT CTEQ CTEP PSIND CAReq CARSp / AUX_SYNC_IND AUX_SCAN_REQ AUX_SCAN_RSP AUX_CONNECT_RSP AUX_CONNECT_REQ LL_MIN_USED_CHANNELS_IND CONTINUOUS LL_CTE_REQ LL_CTE_RSP LL_PERIODIC_SYNC LL_CLOCK_ACCURACY_REQ LL_CLOCK_ACCURACY_RSP \n
			:return: up_type: AIND| ADINd| ANINd| SREQ| SRSP| CREQ| ADCind| DATA| CUReq| CMReq| TIND| EREQ| ERSP| SEReq| SERSp| URSP| FREQ| FRSP| TPACket| PEReq| PERSp| VIND| RIND| PREQ| PRSP| PUIN| LREQ| LRSP| SFR| CPR| CPRS| REIN| PIR| PIRS| AEINd| AAINd| ACINd| ASINd| ASReq| ASPSp| ACRSp| ACReq| MUCH| CONT| CTEQ| CTEP| PSINd| CAReq| CARSp
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:UPTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpPckType)

	def set_up_type(self, up_type: enums.BtoUlpPckType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:UPTYpe \n
		Snippet: driver.source.bb.btooth.set_up_type(up_type = enums.BtoUlpPckType.AAINd) \n
		Selects the packet type. The available packets depend on the selected channel type and installed options. The tables
		below provide an overview. For more information, see data sheet. R&S SMBVB-K60 packet/PDU types
			Table Header: <UpType> / Packet/PDU type \n
			- AIND ADINd ANINd SREQ SRSP CREQ ADCind DATA CUReq CMReq TIND EREQ / ADV_IND ADV_DIRECT_IND ADV_NONCONN_IND SCAN_REQ SCAN_RSP CONNECT_IND ADV_SCAN_IND DATA LL_CONNECTION_UPDATE_IND LL_CHANNEL_MAP_IND LL_TERMINATE_IND LL_ENC_REQ
			- ERSP SEReq SERSp URSP FREQ FRSP TPACket PEReq PERSp VIND RIND / LL_ENC_RSP LL_START_ENC_REQ LL_START_ENC_RSP LL_UNKNONW_RSP LL_FEATURE_REQ LL_FEATURE_RSP TEST PACKET LL_PAUSE_ENC_REQ LL_PAUSE_ENC_RSP LL_VERSION_IND LL_REJECT_IND
		R&S SMBVB-K117 packet/PDU types
			Table Header: <UpType> / Packet/PDU type \n
			- PREQ PRSP PUIN LRSP SFR CPR CPRS REIN PIR PIRS AEINd AAINd ACINd / LL_PHY_REQ LL_PHY_RSP LL_PHY_UPDATE_IND LL_LENGTH_RSP LL_PERIPHERAL_FEATURE_REQ LL_CONNECTION_PARAM_REQ LL_CONNECTION_PARAM_RSP LL_REJECT_EXT_IND LL_PING_REQ LL_PING_RSP ADV_EXT_IND AUX_ADV_IND AUX_CHAIN_IND
			- ASINd ASReq ASPSp ACRSp ACReq MUCH CONT CTEQ CTEP PSIND CAReq CARSp / AUX_SYNC_IND AUX_SCAN_REQ AUX_SCAN_RSP AUX_CONNECT_RSP AUX_CONNECT_REQ LL_MIN_USED_CHANNELS_IND CONTINUOUS LL_CTE_REQ LL_CTE_RSP LL_PERIODIC_SYNC LL_CLOCK_ACCURACY_REQ LL_CLOCK_ACCURACY_RSP \n
			:param up_type: AIND| ADINd| ANINd| SREQ| SRSP| CREQ| ADCind| DATA| CUReq| CMReq| TIND| EREQ| ERSP| SEReq| SERSp| URSP| FREQ| FRSP| TPACket| PEReq| PERSp| VIND| RIND| PREQ| PRSP| PUIN| LREQ| LRSP| SFR| CPR| CPRS| REIN| PIR| PIRS| AEINd| AAINd| ACINd| ASINd| ASReq| ASPSp| ACRSp| ACReq| MUCH| CONT| CTEQ| CTEP| PSINd| CAReq| CARSp
		"""
		param = Conversions.enum_scalar_to_str(up_type, enums.BtoUlpPckType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:UPTYpe {param}')

	def get_us_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:USLength \n
		Snippet: value: int = driver.source.bb.btooth.get_us_length() \n
		Selects the number of frames or events depending on the packet type. The signal repeats after the specified number of
		frames/events. For SCAN_REQ and CONNECT_IND packet, the sequence length is expressed in 'Frames'. For AUX_SCAN_REQ and
		AUX_CONNECT_REQ packet, the sequence length is expressed in 'Frames'. For LL_TERMINATE_IND packets, a default value
		according to the specification is given: Central: PeripheralLatency + 6 Peripheral: 6 For all other packet types the
		sequence length is expressed in 'Events'. \n
			:return: us_length: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:USLength?')
		return Conversions.str_to_int(response)

	def set_us_length(self, us_length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:USLength \n
		Snippet: driver.source.bb.btooth.set_us_length(us_length = 1) \n
		Selects the number of frames or events depending on the packet type. The signal repeats after the specified number of
		frames/events. For SCAN_REQ and CONNECT_IND packet, the sequence length is expressed in 'Frames'. For AUX_SCAN_REQ and
		AUX_CONNECT_REQ packet, the sequence length is expressed in 'Frames'. For LL_TERMINATE_IND packets, a default value
		according to the specification is given: Central: PeripheralLatency + 6 Peripheral: 6 For all other packet types the
		sequence length is expressed in 'Events'. \n
			:param us_length: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		param = Conversions.decimal_value_to_str(us_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:USLength {param}')

	def get_version(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:VERSion \n
		Snippet: value: str = driver.source.bb.btooth.get_version() \n
		Queries the version of the specification for Bluetooth wireless technology underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:VERSion?')
		return trim_str_response(response)

	def clone(self) -> 'BtoothCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BtoothCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
