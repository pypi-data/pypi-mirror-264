from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCls:
	"""Iq commands group definition. 182 total commands, 6 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iq", core, parent)

	@property
	def doherty(self):
		"""doherty commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_doherty'):
			from .Doherty import DohertyCls
			self._doherty = DohertyCls(self._core, self._cmd_group)
		return self._doherty

	@property
	def dpd(self):
		"""dpd commands group. 9 Sub-classes, 5 commands."""
		if not hasattr(self, '_dpd'):
			from .Dpd import DpdCls
			self._dpd = DpdCls(self._core, self._cmd_group)
		return self._dpd

	@property
	def emixer(self):
		"""emixer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_emixer'):
			from .Emixer import EmixerCls
			self._emixer = EmixerCls(self._core, self._cmd_group)
		return self._emixer

	@property
	def impairment(self):
		"""impairment commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_impairment'):
			from .Impairment import ImpairmentCls
			self._impairment = ImpairmentCls(self._core, self._cmd_group)
		return self._impairment

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def swap(self):
		"""swap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swap'):
			from .Swap import SwapCls
			self._swap = SwapCls(self._core, self._cmd_group)
		return self._swap

	def get_crest_factor(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:CREStfactor \n
		Snippet: value: float = driver.source.iq.get_crest_factor() \n
		Specifies the crest factor for the external analog signal. \n
			:return: crest_factor: float Range: 0 to 35, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:CREStfactor?')
		return Conversions.str_to_float(response)

	def set_crest_factor(self, crest_factor: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:CREStfactor \n
		Snippet: driver.source.iq.set_crest_factor(crest_factor = 1.0) \n
		Specifies the crest factor for the external analog signal. \n
			:param crest_factor: float Range: 0 to 35, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(crest_factor)
		self._core.io.write(f'SOURce<HwInstance>:IQ:CREStfactor {param}')

	# noinspection PyTypeChecker
	def get_gain(self) -> enums.IqGain:
		"""SCPI: [SOURce<HW>]:IQ:GAIN \n
		Snippet: value: enums.IqGain = driver.source.iq.get_gain() \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:return: gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:GAIN?')
		return Conversions.str_to_scalar_enum(response, enums.IqGain)

	def set_gain(self, gain: enums.IqGain) -> None:
		"""SCPI: [SOURce<HW>]:IQ:GAIN \n
		Snippet: driver.source.iq.set_gain(gain = enums.IqGain.DB0) \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:param gain: DBM4| DBM2| DB0| DB2| DB4| DB8| DB6 Dynamic range of 16 dB divided into 2 dB steps. DB0|DB2|DB4|DB6|DB8 Activates the specified gain of 0 dB, +2 dB, +4 dB, +6 dB, +8 dB DBM2|DBM4 Activates the specified gain of -2 dB, -4 dB
		"""
		param = Conversions.enum_scalar_to_str(gain, enums.IqGain)
		self._core.io.write(f'SOURce<HwInstance>:IQ:GAIN {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.IqMode:
		"""SCPI: [SOURce<HW>]:IQ:SOURce \n
		Snippet: value: enums.IqMode = driver.source.iq.get_source() \n
		Selects the input signal source for the I/Q modulator. \n
			:return: source: BASeband| ANALog External signals disable the amplitude modulation, an enabled custom digital modulation, any configured digital standard or an applied digital baseband input signal.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.IqMode)

	def set_source(self, source: enums.IqMode) -> None:
		"""SCPI: [SOURce<HW>]:IQ:SOURce \n
		Snippet: driver.source.iq.set_source(source = enums.IqMode.ANALog) \n
		Selects the input signal source for the I/Q modulator. \n
			:param source: BASeband| ANALog External signals disable the amplitude modulation, an enabled custom digital modulation, any configured digital standard or an applied digital baseband input signal.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.IqMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:STATe \n
		Snippet: value: bool = driver.source.iq.get_state() \n
		Enables/disables the I/Q modulation. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + OUTPut<hw>:STATe or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:STATe \n
		Snippet: driver.source.iq.set_state(state = False) \n
		Enables/disables the I/Q modulation. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + OUTPut<hw>:STATe or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:STATe {param}')

	def get_wb_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:WBSTate \n
		Snippet: value: bool = driver.source.iq.get_wb_state() \n
		Activates I/Q wideband mode. Activation automatically optimizes the settings for wideband modulation signals with a
		bandwidth that is higher then 5 MHz. \n
			:return: wb_state: 1| ON| 0| OFF *RST: 0 (R&S SMBVB-K524) / 1 (R&S SMBVB-K525)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:WBSTate?')
		return Conversions.str_to_bool(response)

	def set_wb_state(self, wb_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:WBSTate \n
		Snippet: driver.source.iq.set_wb_state(wb_state = False) \n
		Activates I/Q wideband mode. Activation automatically optimizes the settings for wideband modulation signals with a
		bandwidth that is higher then 5 MHz. \n
			:param wb_state: 1| ON| 0| OFF *RST: 0 (R&S SMBVB-K524) / 1 (R&S SMBVB-K525)
		"""
		param = Conversions.bool_to_str(wb_state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:WBSTate {param}')

	def clone(self) -> 'IqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
