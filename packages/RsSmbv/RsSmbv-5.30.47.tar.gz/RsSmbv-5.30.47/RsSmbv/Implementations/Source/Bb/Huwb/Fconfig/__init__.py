from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FconfigCls:
	"""Fconfig commands group definition. 24 total commands, 5 Subgroups, 17 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fconfig", core, parent)

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dlength(self):
		"""dlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlength'):
			from .Dlength import DlengthCls
			self._dlength = DlengthCls(self._core, self._cmd_group)
		return self._dlength

	@property
	def fpayload(self):
		"""fpayload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fpayload'):
			from .Fpayload import FpayloadCls
			self._fpayload = FpayloadCls(self._core, self._cmd_group)
		return self._fpayload

	@property
	def fphr(self):
		"""fphr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fphr'):
			from .Fphr import FphrCls
			self._fphr = FphrCls(self._core, self._cmd_group)
		return self._fphr

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Mcs import McsCls
			self._mcs = McsCls(self._core, self._cmd_group)
		return self._mcs

	def get_add_dap(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:ADDGap \n
		Snippet: value: int = driver.source.bb.huwb.fconfig.get_add_dap() \n
		Sets additional gap between payload and STS. \n
			:return: additional_gap: integer Range: 0 to 127
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:ADDGap?')
		return Conversions.str_to_int(response)

	def set_add_dap(self, additional_gap: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:ADDGap \n
		Snippet: driver.source.bb.huwb.fconfig.set_add_dap(additional_gap = 1) \n
		Sets additional gap between payload and STS. \n
			:param additional_gap: integer Range: 0 to 127
		"""
		param = Conversions.decimal_value_to_str(additional_gap)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:ADDGap {param}')

	# noinspection PyTypeChecker
	def get_cindex(self) -> enums.HrpUwbCodeIndex:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:CINDex \n
		Snippet: value: enums.HrpUwbCodeIndex = driver.source.bb.huwb.fconfig.get_cindex() \n
		Sets the code index. \n
			:return: code_index: CI_1| CI_2| CI_3| CI_4| CI_5| CI_6| CI_7| CI_8| CI_9| CI_10| CI_11| CI_12| CI_13| CI_14| CI_15| CI_16| CI_17| CI_18| CI_19| CI_20| CI_21| CI_22| CI_23| CI_24| CI_25| CI_26| CI_27| CI_28| CI_29| CI_30| CI_31| CI_32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:CINDex?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbCodeIndex)

	def set_cindex(self, code_index: enums.HrpUwbCodeIndex) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:CINDex \n
		Snippet: driver.source.bb.huwb.fconfig.set_cindex(code_index = enums.HrpUwbCodeIndex.CI_1) \n
		Sets the code index. \n
			:param code_index: CI_1| CI_2| CI_3| CI_4| CI_5| CI_6| CI_7| CI_8| CI_9| CI_10| CI_11| CI_12| CI_13| CI_14| CI_15| CI_16| CI_17| CI_18| CI_19| CI_20| CI_21| CI_22| CI_23| CI_24| CI_25| CI_26| CI_27| CI_28| CI_29| CI_30| CI_31| CI_32
		"""
		param = Conversions.enum_scalar_to_str(code_index, enums.HrpUwbCodeIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:CINDex {param}')

	# noinspection PyTypeChecker
	def get_cp_burst(self) -> enums.HrpUwbChipsPerBurst:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:CPBurst \n
		Snippet: value: enums.HrpUwbChipsPerBurst = driver.source.bb.huwb.fconfig.get_cp_burst() \n
		Sets the chips per burst. \n
			:return: chips_per_burst: CPB_1| CPB_2| CPB_4| CPB_16| CPB_8| CPB_32| CPB_64| CPB_128| CPB_512
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:CPBurst?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbChipsPerBurst)

	def set_cp_burst(self, chips_per_burst: enums.HrpUwbChipsPerBurst) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:CPBurst \n
		Snippet: driver.source.bb.huwb.fconfig.set_cp_burst(chips_per_burst = enums.HrpUwbChipsPerBurst.CPB_1) \n
		Sets the chips per burst. \n
			:param chips_per_burst: CPB_1| CPB_2| CPB_4| CPB_16| CPB_8| CPB_32| CPB_64| CPB_128| CPB_512
		"""
		param = Conversions.enum_scalar_to_str(chips_per_burst, enums.HrpUwbChipsPerBurst)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:CPBurst {param}')

	def get_da_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DALEngth \n
		Snippet: value: int = driver.source.bb.huwb.fconfig.get_da_length() \n
		Sets the data length of the physical header data in octets. \n
			:return: dlength: integer Range: 1 to 4096
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:DALEngth?')
		return Conversions.str_to_int(response)

	def set_da_length(self, dlength: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DALEngth \n
		Snippet: driver.source.bb.huwb.fconfig.set_da_length(dlength = 1) \n
		Sets the data length of the physical header data in octets. \n
			:param dlength: integer Range: 1 to 4096
		"""
		param = Conversions.decimal_value_to_str(dlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:DALEngth {param}')

	def get_dr(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DR \n
		Snippet: value: float = driver.source.bb.huwb.fconfig.get_dr() \n
		Queries the data rate. \n
			:return: hrp_uwb_data_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:DR?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_hop_burst(self) -> enums.HrpUwbHopBurst:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:HOPBurst \n
		Snippet: value: enums.HrpUwbHopBurst = driver.source.bb.huwb.fconfig.get_hop_burst() \n
		Sets the number of hop bursts. \n
			:return: hop_burst: HB_2| HB_8| HB_32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:HOPBurst?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbHopBurst)

	def set_hop_burst(self, hop_burst: enums.HrpUwbHopBurst) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:HOPBurst \n
		Snippet: driver.source.bb.huwb.fconfig.set_hop_burst(hop_burst = enums.HrpUwbHopBurst.HB_2) \n
		Sets the number of hop bursts. \n
			:param hop_burst: HB_2| HB_8| HB_32
		"""
		param = Conversions.enum_scalar_to_str(hop_burst, enums.HrpUwbHopBurst)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:HOPBurst {param}')

	# noinspection PyTypeChecker
	def get_mdl(self) -> enums.HrpUwbMaxDataLength:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:MDL \n
		Snippet: value: enums.HrpUwbMaxDataLength = driver.source.bb.huwb.fconfig.get_mdl() \n
		Sets the maximum data length for HPRF mode. \n
			:return: max_data_len: MDL_1023| MDL_2047| MDL_4095 MDL_1023 1023 octets MDL_2047 2047 octets MDL_4095 4095 octets
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:MDL?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMaxDataLength)

	def set_mdl(self, max_data_len: enums.HrpUwbMaxDataLength) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:MDL \n
		Snippet: driver.source.bb.huwb.fconfig.set_mdl(max_data_len = enums.HrpUwbMaxDataLength.MDL_1023) \n
		Sets the maximum data length for HPRF mode. \n
			:param max_data_len: MDL_1023| MDL_2047| MDL_4095 MDL_1023 1023 octets MDL_2047 2047 octets MDL_4095 4095 octets
		"""
		param = Conversions.enum_scalar_to_str(max_data_len, enums.HrpUwbMaxDataLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:MDL {param}')

	# noinspection PyTypeChecker
	def get_mfl(self) -> enums.HrpUwbMacFcsLength:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:MFL \n
		Snippet: value: enums.HrpUwbMacFcsLength = driver.source.bb.huwb.fconfig.get_mfl() \n
		Sets the length of the frame check sequence field. \n
			:return: mac_fcs_len: MFL_2| MFL_4 MFL_2 Two octets MFL_4 Four octets
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:MFL?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMacFcsLength)

	def set_mfl(self, mac_fcs_len: enums.HrpUwbMacFcsLength) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:MFL \n
		Snippet: driver.source.bb.huwb.fconfig.set_mfl(mac_fcs_len = enums.HrpUwbMacFcsLength.MFL_2) \n
		Sets the length of the frame check sequence field. \n
			:param mac_fcs_len: MFL_2| MFL_4 MFL_2 Two octets MFL_4 Four octets
		"""
		param = Conversions.enum_scalar_to_str(mac_fcs_len, enums.HrpUwbMacFcsLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:MFL {param}')

	def get_mprf(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:MPRF \n
		Snippet: value: float = driver.source.bb.huwb.fconfig.get_mprf() \n
		Queries the mean pulse repetition frequency (PRF) . \n
			:return: mean_prf: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:MPRF?')
		return Conversions.str_to_float(response)

	def get_phrb_rate(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:PHRBrate \n
		Snippet: value: float = driver.source.bb.huwb.fconfig.get_phrb_rate() \n
		Queries the physical header bit rate. \n
			:return: hrp_uwb_phr_bitrate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:PHRBrate?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_phr_length(self) -> enums.ZigBeePhrLengthInSymbols:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:PHRLength \n
		Snippet: value: enums.ZigBeePhrLengthInSymbols = driver.source.bb.huwb.fconfig.get_phr_length() \n
		No command help available \n
			:return: phr_length: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:PHRLength?')
		return Conversions.str_to_scalar_enum(response, enums.ZigBeePhrLengthInSymbols)

	# noinspection PyTypeChecker
	def get_sfd_length(self) -> enums.HrpUwbSfdlEngth:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:SFDLength \n
		Snippet: value: enums.HrpUwbSfdlEngth = driver.source.bb.huwb.fconfig.get_sfd_length() \n
		Queries the symbol length of the start-of-frame delimiter (SFD) . The SFD length depends on the set SFD symbol sequence,
		see Table 'SFD: indices and lengths'. \n
			:return: sfd_length: SFDL_4| SFDL_8| SFDL_16| SFDL_32| SFDL_64
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:SFDLength?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbSfdlEngth)

	def set_sfd_length(self, sfd_length: enums.HrpUwbSfdlEngth) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:SFDLength \n
		Snippet: driver.source.bb.huwb.fconfig.set_sfd_length(sfd_length = enums.HrpUwbSfdlEngth.SFDL_16) \n
		Queries the symbol length of the start-of-frame delimiter (SFD) . The SFD length depends on the set SFD symbol sequence,
		see Table 'SFD: indices and lengths'. \n
			:param sfd_length: SFDL_4| SFDL_8| SFDL_16| SFDL_32| SFDL_64
		"""
		param = Conversions.enum_scalar_to_str(sfd_length, enums.HrpUwbSfdlEngth)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:SFDLength {param}')

	# noinspection PyTypeChecker
	def get_sf_payload(self) -> enums.ZigBeeSpreadingFactor:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:SFPAYLoad \n
		Snippet: value: enums.ZigBeeSpreadingFactor = driver.source.bb.huwb.fconfig.get_sf_payload() \n
		No command help available \n
			:return: factor_in_payload: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:SFPAYLoad?')
		return Conversions.str_to_scalar_enum(response, enums.ZigBeeSpreadingFactor)

	# noinspection PyTypeChecker
	def get_sf_shr(self) -> enums.ZigBeeSpreadingFactor:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:SFShr \n
		Snippet: value: enums.ZigBeeSpreadingFactor = driver.source.bb.huwb.fconfig.get_sf_shr() \n
		No command help available \n
			:return: sfi_nshr: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:SFShr?')
		return Conversions.str_to_scalar_enum(response, enums.ZigBeeSpreadingFactor)

	def get_sym_rate(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:SYMRate \n
		Snippet: value: float = driver.source.bb.huwb.fconfig.get_sym_rate() \n
		No command help available \n
			:return: hrp_uwb_symbol_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:SYMRate?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_syn_length(self) -> enums.HrpUwbSyncLength:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:SYNLength \n
		Snippet: value: enums.HrpUwbSyncLength = driver.source.bb.huwb.fconfig.get_syn_length() \n
		Sets the sync length. \n
			:return: sync_length: SL_16| SL_24| SL_32| SL_48| SL_64| SL_96| SL_128| SL_256| SL_1024| SL_4096
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:SYNLength?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbSyncLength)

	def set_syn_length(self, sync_length: enums.HrpUwbSyncLength) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:SYNLength \n
		Snippet: driver.source.bb.huwb.fconfig.set_syn_length(sync_length = enums.HrpUwbSyncLength.SL_1024) \n
		Sets the sync length. \n
			:param sync_length: SL_16| SL_24| SL_32| SL_48| SL_64| SL_96| SL_128| SL_256| SL_1024| SL_4096
		"""
		param = Conversions.enum_scalar_to_str(sync_length, enums.HrpUwbSyncLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:SYNLength {param}')

	# noinspection PyTypeChecker
	def get_vrate(self) -> enums.HrpUwbViterbiRate:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:VRATe \n
		Snippet: value: enums.HrpUwbViterbiRate = driver.source.bb.huwb.fconfig.get_vrate() \n
		Queries the viterbi rate for convolutional coding. \n
			:return: hrp_uwb_viterbi_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:VRATe?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbViterbiRate)

	def clone(self) -> 'FconfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FconfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
