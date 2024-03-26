from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CdataCls:
	"""Cdata commands group definition. 51 total commands, 4 Subgroups, 44 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cdata", core, parent)

	@property
	def ccid(self):
		"""ccid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccid'):
			from .Ccid import CcidCls
			self._ccid = CcidCls(self._core, self._cmd_group)
		return self._ccid

	@property
	def ecode(self):
		"""ecode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecode'):
			from .Ecode import EcodeCls
			self._ecode = EcodeCls(self._core, self._cmd_group)
		return self._ecode

	@property
	def bposition(self):
		"""bposition commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bposition'):
			from .Bposition import BpositionCls
			self._bposition = BpositionCls(self._core, self._cmd_group)
		return self._bposition

	@property
	def channel(self):
		"""channel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	# noinspection PyTypeChecker
	def get_aci(self) -> enums.BtoCsCtrlAci:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ACI \n
		Snippet: value: enums.BtoCsCtrlAci = driver.source.bb.btooth.cs.cdata.get_aci() \n
		No command help available \n
			:return: aci: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ACI?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAci)

	def set_aci(self, aci: enums.BtoCsCtrlAci) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ACI \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_aci(aci = enums.BtoCsCtrlAci.ACI0) \n
		No command help available \n
			:param aci: No help available
		"""
		param = Conversions.enum_scalar_to_str(aci, enums.BtoCsCtrlAci)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ACI {param}')

	def get_ce_count(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CECount \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_ce_count() \n
		No command help available \n
			:return: conn_event_count: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CECount?')
		return Conversions.str_to_int(response)

	def set_ce_count(self, conn_event_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CECount \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ce_count(conn_event_count = 1) \n
		No command help available \n
			:param conn_event_count: No help available
		"""
		param = Conversions.decimal_value_to_str(conn_event_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CECount {param}')

	def get_cid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CID \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_cid() \n
		No command help available \n
			:return: config_id: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CID?')
		return Conversions.str_to_int(response)

	def set_cid(self, config_id: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CID \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_cid(config_id = 1) \n
		No command help available \n
			:param config_id: No help available
		"""
		param = Conversions.decimal_value_to_str(config_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CID {param}')

	def get_csa_threec(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSAThreec \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_csa_threec() \n
		No command help available \n
			:return: csa_threec: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSAThreec?')
		return Conversions.str_to_bool(response)

	def set_csa_threec(self, csa_threec: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSAThreec \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_csa_threec(csa_threec = False) \n
		No command help available \n
			:param csa_threec: No help available
		"""
		param = Conversions.bool_to_str(csa_threec)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSAThreec {param}')

	def get_csignal(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSIGnal \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_csignal() \n
		No command help available \n
			:return: companion_signal: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSIGnal?')
		return Conversions.str_to_bool(response)

	def set_csignal(self, companion_signal: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSIGnal \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_csignal(companion_signal = False) \n
		No command help available \n
			:param companion_signal: No help available
		"""
		param = Conversions.bool_to_str(companion_signal)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSIGnal {param}')

	# noinspection PyTypeChecker
	def get_csp_capability(self) -> enums.BtoCsCtrlSyncPhy:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:CSPCapability \n
		Snippet: value: enums.BtoCsCtrlSyncPhy = driver.source.bb.btooth.cs.cdata.get_csp_capability() \n
		No command help available \n
			:return: sync_phy: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CSPCapability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlSyncPhy)

	def get_eoffset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:EOFFset \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_eoffset() \n
		No command help available \n
			:return: event_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:EOFFset?')
		return Conversions.str_to_int(response)

	def set_eoffset(self, event_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:EOFFset \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_eoffset(event_offset = 1) \n
		No command help available \n
			:param event_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(event_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:EOFFset {param}')

	def get_ma_path(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MAPath \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_ma_path() \n
		No command help available \n
			:return: max_ant_path: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MAPath?')
		return Conversions.str_to_int(response)

	def set_ma_path(self, max_ant_path: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MAPath \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ma_path(max_ant_path = 1) \n
		No command help available \n
			:param max_ant_path: No help available
		"""
		param = Conversions.decimal_value_to_str(max_ant_path)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MAPath {param}')

	def get_mma_steps(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMASteps \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mma_steps() \n
		No command help available \n
			:return: mm_max_steps: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMASteps?')
		return Conversions.str_to_int(response)

	def set_mma_steps(self, mm_max_steps: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMASteps \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mma_steps(mm_max_steps = 1) \n
		No command help available \n
			:param mm_max_steps: No help available
		"""
		param = Conversions.decimal_value_to_str(mm_max_steps)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMASteps {param}')

	def get_mmi_steps(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMISteps \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mmi_steps() \n
		No command help available \n
			:return: mm_min_steps: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMISteps?')
		return Conversions.str_to_int(response)

	def set_mmi_steps(self, mm_min_steps: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMISteps \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mmi_steps(mm_min_steps = 1) \n
		No command help available \n
			:param mm_min_steps: No help available
		"""
		param = Conversions.decimal_value_to_str(mm_min_steps)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMISteps {param}')

	# noinspection PyTypeChecker
	def get_mmode(self) -> enums.BtoCsMainMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMODe \n
		Snippet: value: enums.BtoCsMainMode = driver.source.bb.btooth.cs.cdata.get_mmode() \n
		No command help available \n
			:return: main_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsMainMode)

	def set_mmode(self, main_mode: enums.BtoCsMainMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMODe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mmode(main_mode = enums.BtoCsMainMode.MODE1) \n
		No command help available \n
			:param main_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(main_mode, enums.BtoCsMainMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMODe {param}')

	def get_mm_repetition(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMRepetition \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mm_repetition() \n
		No command help available \n
			:return: mm_repetition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMRepetition?')
		return Conversions.str_to_int(response)

	def set_mm_repetition(self, mm_repetition: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MMRepetition \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mm_repetition(mm_repetition = 1) \n
		No command help available \n
			:param mm_repetition: No help available
		"""
		param = Conversions.decimal_value_to_str(mm_repetition)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MMRepetition {param}')

	def get_mp_length(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPLength \n
		Snippet: value: float = driver.source.bb.btooth.cs.cdata.get_mp_length() \n
		No command help available \n
			:return: mp_length: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPLength?')
		return Conversions.str_to_float(response)

	def set_mp_length(self, mp_length: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPLength \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mp_length(mp_length = 1.0) \n
		No command help available \n
			:param mp_length: No help available
		"""
		param = Conversions.decimal_value_to_str(mp_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPLength {param}')

	def get_mp_supported(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPSupported \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mp_supported() \n
		No command help available \n
			:return: mp_supported: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPSupported?')
		return Conversions.str_to_int(response)

	def set_mp_supported(self, mp_supported: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MPSupported \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mp_supported(mp_supported = 1) \n
		No command help available \n
			:param mp_supported: No help available
		"""
		param = Conversions.decimal_value_to_str(mp_supported)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MPSupported {param}')

	# noinspection PyTypeChecker
	def get_mtype(self) -> enums.BtoCsCtrlModeType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MTYPe \n
		Snippet: value: enums.BtoCsCtrlModeType = driver.source.bb.btooth.cs.cdata.get_mtype() \n
		No command help available \n
			:return: mode_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlModeType)

	def get_mz_steps(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MZSTeps \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_mz_steps() \n
		No command help available \n
			:return: mode_0_steps: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MZSTeps?')
		return Conversions.str_to_int(response)

	def set_mz_steps(self, mode_0_steps: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:MZSTeps \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_mz_steps(mode_0_steps = 1) \n
		No command help available \n
			:param mode_0_steps: No help available
		"""
		param = Conversions.decimal_value_to_str(mode_0_steps)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:MZSTeps {param}')

	def get_nant(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NANT \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_nant() \n
		No command help available \n
			:return: num_ant: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NANT?')
		return Conversions.str_to_int(response)

	def set_nant(self, num_ant: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NANT \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nant(num_ant = 1) \n
		No command help available \n
			:param num_ant: No help available
		"""
		param = Conversions.decimal_value_to_str(num_ant)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NANT {param}')

	def get_nconfig(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NCONfig \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_nconfig() \n
		No command help available \n
			:return: num_config: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NCONfig?')
		return Conversions.str_to_int(response)

	def set_nconfig(self, num_config: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NCONfig \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nconfig(num_config = 1) \n
		No command help available \n
			:param num_config: No help available
		"""
		param = Conversions.decimal_value_to_str(num_config)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NCONfig {param}')

	def get_nfae(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NFAE \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_nfae() \n
		No command help available \n
			:return: no_fae: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NFAE?')
		return Conversions.str_to_bool(response)

	def set_nfae(self, no_fae: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NFAE \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nfae(no_fae = False) \n
		No command help available \n
			:param no_fae: No help available
		"""
		param = Conversions.bool_to_str(no_fae)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NFAE {param}')

	# noinspection PyTypeChecker
	def get_nrs_capability(self) -> enums.BtoCsCtrlNadm:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NRSCapability \n
		Snippet: value: enums.BtoCsCtrlNadm = driver.source.bb.btooth.cs.cdata.get_nrs_capability() \n
		No command help available \n
			:return: nrs_capability: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NRSCapability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlNadm)

	def set_nrs_capability(self, nrs_capability: enums.BtoCsCtrlNadm) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NRSCapability \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_nrs_capability(nrs_capability = enums.BtoCsCtrlNadm.NADM) \n
		No command help available \n
			:param nrs_capability: No help available
		"""
		param = Conversions.enum_scalar_to_str(nrs_capability, enums.BtoCsCtrlNadm)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NRSCapability {param}')

	# noinspection PyTypeChecker
	def get_ns_capability(self) -> enums.BtoCsCtrlNadm:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NSCapability \n
		Snippet: value: enums.BtoCsCtrlNadm = driver.source.bb.btooth.cs.cdata.get_ns_capability() \n
		No command help available \n
			:return: ns_capability: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NSCapability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlNadm)

	def set_ns_capability(self, ns_capability: enums.BtoCsCtrlNadm) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:NSCapability \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ns_capability(ns_capability = enums.BtoCsCtrlNadm.NADM) \n
		No command help available \n
			:param ns_capability: No help available
		"""
		param = Conversions.enum_scalar_to_str(ns_capability, enums.BtoCsCtrlNadm)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:NSCapability {param}')

	def get_omax(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMAX \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_omax() \n
		No command help available \n
			:return: offset_max: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMAX?')
		return Conversions.str_to_int(response)

	def set_omax(self, offset_max: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMAX \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_omax(offset_max = 1) \n
		No command help available \n
			:param offset_max: No help available
		"""
		param = Conversions.decimal_value_to_str(offset_max)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMAX {param}')

	def get_omin(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMIN \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_omin() \n
		No command help available \n
			:return: offset_min: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMIN?')
		return Conversions.str_to_int(response)

	def set_omin(self, offset_min: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:OMIN \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_omin(offset_min = 1) \n
		No command help available \n
			:param offset_min: No help available
		"""
		param = Conversions.decimal_value_to_str(offset_min)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:OMIN {param}')

	def get_pcount(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PCOunt \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_pcount() \n
		No command help available \n
			:return: proc_count: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PCOunt?')
		return Conversions.str_to_int(response)

	def set_pcount(self, proc_count: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PCOunt \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pcount(proc_count = 1) \n
		No command help available \n
			:param proc_count: No help available
		"""
		param = Conversions.decimal_value_to_str(proc_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PCOunt {param}')

	def get_pdelta(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PDELta \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_pdelta() \n
		No command help available \n
			:return: pwr_delta: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PDELta?')
		return Conversions.str_to_int(response)

	def set_pdelta(self, pwr_delta: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PDELta \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pdelta(pwr_delta = 1) \n
		No command help available \n
			:param pwr_delta: No help available
		"""
		param = Conversions.decimal_value_to_str(pwr_delta)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PDELta {param}')

	# noinspection PyTypeChecker
	def get_phy(self) -> enums.BtoPackFormat:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PHY \n
		Snippet: value: enums.BtoPackFormat = driver.source.bb.btooth.cs.cdata.get_phy() \n
		No command help available \n
			:return: phy: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PHY?')
		return Conversions.str_to_scalar_enum(response, enums.BtoPackFormat)

	def get_pinterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_pinterval() \n
		No command help available \n
			:return: proc_interval: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PINTerval?')
		return Conversions.str_to_int(response)

	def set_pinterval(self, proc_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PINTerval \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pinterval(proc_interval = 1) \n
		No command help available \n
			:param proc_interval: No help available
		"""
		param = Conversions.decimal_value_to_str(proc_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PINTerval {param}')

	# noinspection PyTypeChecker
	def get_pp_antenna(self) -> enums.BtoCsCtrlAnt:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PPANtenna \n
		Snippet: value: enums.BtoCsCtrlAnt = driver.source.bb.btooth.cs.cdata.get_pp_antenna() \n
		No command help available \n
			:return: pp_antenna: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PPANtenna?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAnt)

	def set_pp_antenna(self, pp_antenna: enums.BtoCsCtrlAnt) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:PPANtenna \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_pp_antenna(pp_antenna = enums.BtoCsCtrlAnt.ANT0) \n
		No command help available \n
			:param pp_antenna: No help available
		"""
		param = Conversions.enum_scalar_to_str(pp_antenna, enums.BtoCsCtrlAnt)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:PPANtenna {param}')

	# noinspection PyTypeChecker
	def get_ra_only(self) -> enums.BtoCsCtrlAccReq:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RAONly \n
		Snippet: value: enums.BtoCsCtrlAccReq = driver.source.bb.btooth.cs.cdata.get_ra_only() \n
		No command help available \n
			:return: rtt_aa_only: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RAONly?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAccReq)

	def set_ra_only(self, rtt_aa_only: enums.BtoCsCtrlAccReq) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RAONly \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ra_only(rtt_aa_only = enums.BtoCsCtrlAccReq.AR0) \n
		No command help available \n
			:param rtt_aa_only: No help available
		"""
		param = Conversions.enum_scalar_to_str(rtt_aa_only, enums.BtoCsCtrlAccReq)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RAONly {param}')

	# noinspection PyTypeChecker
	def get_rcapability(self) -> enums.BtoCsCtrlRttCap:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RCAPability \n
		Snippet: value: enums.BtoCsCtrlRttCap = driver.source.bb.btooth.cs.cdata.get_rcapability() \n
		No command help available \n
			:return: rtt_capability: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RCAPability?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlRttCap)

	def set_rcapability(self, rtt_capability: enums.BtoCsCtrlRttCap) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RCAPability \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rcapability(rtt_capability = enums.BtoCsCtrlRttCap.CAP0) \n
		No command help available \n
			:param rtt_capability: No help available
		"""
		param = Conversions.enum_scalar_to_str(rtt_capability, enums.BtoCsCtrlRttCap)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RCAPability {param}')

	def get_rfu(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RFU \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_rfu() \n
		No command help available \n
			:return: rfu: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RFU?')
		return Conversions.str_to_int(response)

	def set_rfu(self, rfu: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RFU \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rfu(rfu = 1) \n
		No command help available \n
			:param rfu: No help available
		"""
		param = Conversions.decimal_value_to_str(rfu)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RFU {param}')

	# noinspection PyTypeChecker
	def get_rr_sequence(self) -> enums.BtoCsCtrlAccReq:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RRSequence \n
		Snippet: value: enums.BtoCsCtrlAccReq = driver.source.bb.btooth.cs.cdata.get_rr_sequence() \n
		No command help available \n
			:return: rr_sequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RRSequence?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAccReq)

	def set_rr_sequence(self, rr_sequence: enums.BtoCsCtrlAccReq) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RRSequence \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rr_sequence(rr_sequence = enums.BtoCsCtrlAccReq.AR0) \n
		No command help available \n
			:param rr_sequence: No help available
		"""
		param = Conversions.enum_scalar_to_str(rr_sequence, enums.BtoCsCtrlAccReq)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RRSequence {param}')

	# noinspection PyTypeChecker
	def get_rsounding(self) -> enums.BtoCsCtrlAccReq:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RSOunding \n
		Snippet: value: enums.BtoCsCtrlAccReq = driver.source.bb.btooth.cs.cdata.get_rsounding() \n
		No command help available \n
			:return: rsounding: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RSOunding?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlAccReq)

	def set_rsounding(self, rsounding: enums.BtoCsCtrlAccReq) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RSOunding \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rsounding(rsounding = enums.BtoCsCtrlAccReq.AR0) \n
		No command help available \n
			:param rsounding: No help available
		"""
		param = Conversions.enum_scalar_to_str(rsounding, enums.BtoCsCtrlAccReq)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RSOunding {param}')

	# noinspection PyTypeChecker
	def get_rtype(self) -> enums.BtoCsCtrlRttType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RTYPe \n
		Snippet: value: enums.BtoCsCtrlRttType = driver.source.bb.btooth.cs.cdata.get_rtype() \n
		No command help available \n
			:return: rtt_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCtrlRttType)

	def set_rtype(self, rtt_type: enums.BtoCsCtrlRttType) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:RTYPe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_rtype(rtt_type = enums.BtoCsCtrlRttType.R128RS) \n
		No command help available \n
			:param rtt_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(rtt_type, enums.BtoCsCtrlRttType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:RTYPe {param}')

	def get_sinterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_sinterval() \n
		No command help available \n
			:return: sub_interval: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SINTerval?')
		return Conversions.str_to_int(response)

	def set_sinterval(self, sub_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SINTerval \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_sinterval(sub_interval = 1) \n
		No command help available \n
			:param sub_interval: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SINTerval {param}')

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SLENgth \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_slength() \n
		No command help available \n
			:return: sub_length: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, sub_length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SLENgth \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_slength(sub_length = 1) \n
		No command help available \n
			:param sub_length: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.BtoCsSubMode:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SMODe \n
		Snippet: value: enums.BtoCsSubMode = driver.source.bb.btooth.cs.cdata.get_smode() \n
		No command help available \n
			:return: sub_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsSubMode)

	def set_smode(self, sub_mode: enums.BtoCsSubMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SMODe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_smode(sub_mode = enums.BtoCsSubMode.MODE1) \n
		No command help available \n
			:param sub_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(sub_mode, enums.BtoCsSubMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SMODe {param}')

	def get_snumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SNUMber \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.get_snumber() \n
		No command help available \n
			:return: sub_number: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SNUMber?')
		return Conversions.str_to_int(response)

	def set_snumber(self, sub_number: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SNUMber \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_snumber(sub_number = 1) \n
		No command help available \n
			:param sub_number: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SNUMber {param}')

	def get_sp_estimate(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SPEStimate \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.get_sp_estimate() \n
		No command help available \n
			:return: sp_estimate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SPEStimate?')
		return Conversions.str_to_bool(response)

	def set_sp_estimate(self, sp_estimate: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:SPEStimate \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_sp_estimate(sp_estimate = False) \n
		No command help available \n
			:param sp_estimate: No help available
		"""
		param = Conversions.bool_to_str(sp_estimate)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:SPEStimate {param}')

	# noinspection PyTypeChecker
	def get_tfcs(self) -> enums.BtoCsTfcs:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TFCS \n
		Snippet: value: enums.BtoCsTfcs = driver.source.bb.btooth.cs.cdata.get_tfcs() \n
		No command help available \n
			:return: tfcs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TFCS?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTfcs)

	def set_tfcs(self, tfcs: enums.BtoCsTfcs) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TFCS \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_tfcs(tfcs = enums.BtoCsTfcs.TFCS_100) \n
		No command help available \n
			:param tfcs: No help available
		"""
		param = Conversions.enum_scalar_to_str(tfcs, enums.BtoCsTfcs)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TFCS {param}')

	# noinspection PyTypeChecker
	def get_ti_one(self) -> enums.BtoCsTiP1:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TIONe \n
		Snippet: value: enums.BtoCsTiP1 = driver.source.bb.btooth.cs.cdata.get_ti_one() \n
		No command help available \n
			:return: tip_one: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TIONe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP1)

	def set_ti_one(self, tip_one: enums.BtoCsTiP1) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TIONe \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ti_one(tip_one = enums.BtoCsTiP1.TIP1_10) \n
		No command help available \n
			:param tip_one: No help available
		"""
		param = Conversions.enum_scalar_to_str(tip_one, enums.BtoCsTiP1)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TIONe {param}')

	# noinspection PyTypeChecker
	def get_ti_two(self) -> enums.BtoCsTiP1:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TITWo \n
		Snippet: value: enums.BtoCsTiP1 = driver.source.bb.btooth.cs.cdata.get_ti_two() \n
		No command help available \n
			:return: tip_two: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TITWo?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTiP1)

	def set_ti_two(self, tip_two: enums.BtoCsTiP1) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TITWo \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_ti_two(tip_two = enums.BtoCsTiP1.TIP1_10) \n
		No command help available \n
			:param tip_two: No help available
		"""
		param = Conversions.enum_scalar_to_str(tip_two, enums.BtoCsTiP1)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TITWo {param}')

	# noinspection PyTypeChecker
	def get_tpm(self) -> enums.BtoCsTpm:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TPM \n
		Snippet: value: enums.BtoCsTpm = driver.source.bb.btooth.cs.cdata.get_tpm() \n
		No command help available \n
			:return: tpm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TPM?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTpm)

	def set_tpm(self, tpm: enums.BtoCsTpm) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TPM \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_tpm(tpm = enums.BtoCsTpm.TPM_10) \n
		No command help available \n
			:param tpm: No help available
		"""
		param = Conversions.enum_scalar_to_str(tpm, enums.BtoCsTpm)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TPM {param}')

	# noinspection PyTypeChecker
	def get_tsw(self) -> enums.BtoCsTsw:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TSW \n
		Snippet: value: enums.BtoCsTsw = driver.source.bb.btooth.cs.cdata.get_tsw() \n
		No command help available \n
			:return: tsw: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TSW?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTsw)

	def set_tsw(self, tsw: enums.BtoCsTsw) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:TSW \n
		Snippet: driver.source.bb.btooth.cs.cdata.set_tsw(tsw = enums.BtoCsTsw.TSW_0) \n
		No command help available \n
			:param tsw: No help available
		"""
		param = Conversions.enum_scalar_to_str(tsw, enums.BtoCsTsw)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:TSW {param}')

	def clone(self) -> 'CdataCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CdataCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
