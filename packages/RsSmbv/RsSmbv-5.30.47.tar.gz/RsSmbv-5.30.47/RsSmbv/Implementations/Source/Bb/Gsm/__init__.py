from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GsmCls:
	"""Gsm commands group definition. 104 total commands, 17 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gsm", core, parent)

	@property
	def aqPsk(self):
		"""aqPsk commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_aqPsk'):
			from .AqPsk import AqPskCls
			self._aqPsk = AqPskCls(self._core, self._cmd_group)
		return self._aqPsk

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def edge(self):
		"""edge commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_edge'):
			from .Edge import EdgeCls
			self._edge = EdgeCls(self._core, self._cmd_group)
		return self._edge

	@property
	def filterPy(self):
		"""filterPy commands group. 7 Sub-classes, 2 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def frame(self):
		"""frame commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_frame'):
			from .Frame import FrameCls
			self._frame = FrameCls(self._core, self._cmd_group)
		return self._frame

	@property
	def fsk(self):
		"""fsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fsk'):
			from .Fsk import FskCls
			self._fsk = FskCls(self._core, self._cmd_group)
		return self._fsk

	@property
	def h16Qam(self):
		"""h16Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_h16Qam'):
			from .H16Qam import H16QamCls
			self._h16Qam = H16QamCls(self._core, self._cmd_group)
		return self._h16Qam

	@property
	def h32Qam(self):
		"""h32Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_h32Qam'):
			from .H32Qam import H32QamCls
			self._h32Qam = H32QamCls(self._core, self._cmd_group)
		return self._h32Qam

	@property
	def hqpsk(self):
		"""hqpsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hqpsk'):
			from .Hqpsk import HqpskCls
			self._hqpsk = HqpskCls(self._core, self._cmd_group)
		return self._hqpsk

	@property
	def mframe(self):
		"""mframe commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mframe'):
			from .Mframe import MframeCls
			self._mframe = MframeCls(self._core, self._cmd_group)
		return self._mframe

	@property
	def n16Qam(self):
		"""n16Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n16Qam'):
			from .N16Qam import N16QamCls
			self._n16Qam = N16QamCls(self._core, self._cmd_group)
		return self._n16Qam

	@property
	def n32Qam(self):
		"""n32Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n32Qam'):
			from .N32Qam import N32QamCls
			self._n32Qam = N32QamCls(self._core, self._cmd_group)
		return self._n32Qam

	@property
	def pramp(self):
		"""pramp commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_pramp'):
			from .Pramp import PrampCls
			self._pramp = PrampCls(self._core, self._cmd_group)
		return self._pramp

	@property
	def sattenuation(self):
		"""sattenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sattenuation'):
			from .Sattenuation import SattenuationCls
			self._sattenuation = SattenuationCls(self._core, self._cmd_group)
		return self._sattenuation

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 2 commands."""
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

	def get_fone(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GSM:FONE \n
		Snippet: value: bool = driver.source.bb.gsm.get_fone() \n
		A modulating bit stream consisting of consecutive ones is used for inactive slots (according to GSM 05.04) .
		If this parameter is disabled, the inactive slots are filled in with 0. \n
			:return: fone: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FONE?')
		return Conversions.str_to_bool(response)

	def set_fone(self, fone: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:FONE \n
		Snippet: driver.source.bb.gsm.set_fone(fone = False) \n
		A modulating bit stream consisting of consecutive ones is used for inactive slots (according to GSM 05.04) .
		If this parameter is disabled, the inactive slots are filled in with 0. \n
			:param fone: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(fone)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FONE {param}')

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModTypeGsm:
		"""SCPI: [SOURce<HW>]:BB:GSM:FORMat \n
		Snippet: value: enums.GsmModTypeGsm = driver.source.bb.gsm.get_format_py() \n
		The command selects the modulation type. \n
			:return: format_py: MSK| FSK2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModTypeGsm)

	def set_format_py(self, format_py: enums.GsmModTypeGsm) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:FORMat \n
		Snippet: driver.source.bb.gsm.set_format_py(format_py = enums.GsmModTypeGsm.FSK2) \n
		The command selects the modulation type. \n
			:param format_py: MSK| FSK2
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.GsmModTypeGsm)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FORMat {param}')

	def get_is_length(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GSM:ISLength \n
		Snippet: value: bool = driver.source.bb.gsm.get_is_length() \n
		Selects constant slot length. \n
			:return: is_length: 1| ON| 0| OFF For normal symbol rate mode: The command selects whether the 1/4 symbol of a GSM slot is ignored or compensated for by an extra symbol every 4th slot. For higher symbol rate mode: The command selects whether the 1/2 symbol of an average slot with a length of 187.5 symbols are ignored or compensated for by an extra symbol every second slot. ON In normal symbol rate mode, all slots are 156 symbols long In higher symbol rate mode, all slots are 187 symbols long OFF In normal symbol rate mode, some slots are 157 symbols long In higher symbol rate mode, some slots are 188 symbols long
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:ISLength?')
		return Conversions.str_to_bool(response)

	def set_is_length(self, is_length: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:ISLength \n
		Snippet: driver.source.bb.gsm.set_is_length(is_length = False) \n
		Selects constant slot length. \n
			:param is_length: 1| ON| 0| OFF For normal symbol rate mode: The command selects whether the 1/4 symbol of a GSM slot is ignored or compensated for by an extra symbol every 4th slot. For higher symbol rate mode: The command selects whether the 1/2 symbol of an average slot with a length of 187.5 symbols are ignored or compensated for by an extra symbol every second slot. ON In normal symbol rate mode, all slots are 156 symbols long In higher symbol rate mode, all slots are 187 symbols long OFF In normal symbol rate mode, some slots are 157 symbols long In higher symbol rate mode, some slots are 188 symbols long
		"""
		param = Conversions.bool_to_str(is_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:ISLength {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.GsmMode:
		"""SCPI: [SOURce<HW>]:BB:GSM:MODE \n
		Snippet: value: enums.GsmMode = driver.source.bb.gsm.get_mode() \n
		The command selects GSM mode. \n
			:return: mode: UNFRamed| SINGle| DOUBle| MULTiframe UNFRamed Modulation signal without slot and frame structure. SINGle Modulation signal consisting of one frame. DOUBle Modulation signal in which two frames are defined and then combined by some method into a single multiframe signal. MULTiframe Multiframe signal.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.GsmMode)

	def set_mode(self, mode: enums.GsmMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:MODE \n
		Snippet: driver.source.bb.gsm.set_mode(mode = enums.GsmMode.DOUBle) \n
		The command selects GSM mode. \n
			:param mode: UNFRamed| SINGle| DOUBle| MULTiframe UNFRamed Modulation signal without slot and frame structure. SINGle Modulation signal consisting of one frame. DOUBle Modulation signal in which two frames are defined and then combined by some method into a single multiframe signal. MULTiframe Multiframe signal.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.GsmMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:MODE {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:PRESet \n
		Snippet: driver.source.bb.gsm.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:GSM:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:PRESet \n
		Snippet: driver.source.bb.gsm.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:GSM:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GSM:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.GsmSimMode:
		"""SCPI: [SOURce<HW>]:BB:GSM:SMODe \n
		Snippet: value: enums.GsmSimMode = driver.source.bb.gsm.get_smode() \n
		Selects the modulation signal for the mode Unframed (BB:GSM:MODE UNFR) . The modulation type and filter type are set in
		accordance with the selection.
			INTRO_CMD_HELP: The available simulation modes depend on the selected symbol rate: \n
			- Normal Symbol Rate - GSM, EDGE (8PSK) , AQPSK, 16QAM and 32QAM
			- Higher Symbol Rate - HSR QPSK, HSR 16QAM and HSR 32QAM.
		Note:'Higher Symbol Rate' Mode and 'Simulation Modes' AQPSK, 16QAM, 32QAM, HSR QPSK, HSR 16QAM and HSR 32QAM are
		available for instruments equipped with option R&S SMBVB-K41 only. \n
			:return: smode: GSM| EDGE| N16Qam| N32Qam| HQPSk| H16Qam| H32Qam| AQPSk
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.GsmSimMode)

	def set_smode(self, smode: enums.GsmSimMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:SMODe \n
		Snippet: driver.source.bb.gsm.set_smode(smode = enums.GsmSimMode.AQPSk) \n
		Selects the modulation signal for the mode Unframed (BB:GSM:MODE UNFR) . The modulation type and filter type are set in
		accordance with the selection.
			INTRO_CMD_HELP: The available simulation modes depend on the selected symbol rate: \n
			- Normal Symbol Rate - GSM, EDGE (8PSK) , AQPSK, 16QAM and 32QAM
			- Higher Symbol Rate - HSR QPSK, HSR 16QAM and HSR 32QAM.
		Note:'Higher Symbol Rate' Mode and 'Simulation Modes' AQPSK, 16QAM, 32QAM, HSR QPSK, HSR 16QAM and HSR 32QAM are
		available for instruments equipped with option R&S SMBVB-K41 only. \n
			:param smode: GSM| EDGE| N16Qam| N32Qam| HQPSk| H16Qam| H32Qam| AQPSk
		"""
		param = Conversions.enum_scalar_to_str(smode, enums.GsmSimMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:SMODe {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GSM:STATe \n
		Snippet: value: bool = driver.source.bb.gsm.get_state() \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:STATe \n
		Snippet: driver.source.bb.gsm.set_state(state = False) \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:STATe {param}')

	def clone(self) -> 'GsmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GsmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
