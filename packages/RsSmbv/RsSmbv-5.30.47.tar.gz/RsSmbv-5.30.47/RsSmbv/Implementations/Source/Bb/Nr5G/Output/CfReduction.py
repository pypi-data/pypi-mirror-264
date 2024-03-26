from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfReductionCls:
	"""CfReduction commands group definition. 8 total commands, 0 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfReduction", core, parent)

	# noinspection PyTypeChecker
	def get_algorithm(self) -> enums.CrestFactoralgorithm:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ALGorithm \n
		Snippet: value: enums.CrestFactoralgorithm = driver.source.bb.nr5G.output.cfReduction.get_algorithm() \n
		Selects the algorithm used for the crest factor reduction. \n
			:return: cfr_algorithm: CLF Clipping and filtering algorithm PC Peak cancellation algorithm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ALGorithm?')
		return Conversions.str_to_scalar_enum(response, enums.CrestFactoralgorithm)

	def set_algorithm(self, cfr_algorithm: enums.CrestFactoralgorithm) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ALGorithm \n
		Snippet: driver.source.bb.nr5G.output.cfReduction.set_algorithm(cfr_algorithm = enums.CrestFactoralgorithm.CLF) \n
		Selects the algorithm used for the crest factor reduction. \n
			:param cfr_algorithm: CLF Clipping and filtering algorithm PC Peak cancellation algorithm
		"""
		param = Conversions.enum_scalar_to_str(cfr_algorithm, enums.CrestFactoralgorithm)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ALGorithm {param}')

	def get_cp_bwidth(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:CPBWidth \n
		Snippet: value: float = driver.source.bb.nr5G.output.cfReduction.get_cp_bwidth() \n
		Sets the bandwidth of the cancellation pulse.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:OUTPut:CFReduction:ALGorithm = PC \n
			:return: cancel_pulse_bw: float Range: 0 to 500e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:CPBWidth?')
		return Conversions.str_to_float(response)

	def set_cp_bwidth(self, cancel_pulse_bw: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:CPBWidth \n
		Snippet: driver.source.bb.nr5G.output.cfReduction.set_cp_bwidth(cancel_pulse_bw = 1.0) \n
		Sets the bandwidth of the cancellation pulse.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:OUTPut:CFReduction:ALGorithm = PC \n
			:param cancel_pulse_bw: float Range: 0 to 500e6
		"""
		param = Conversions.decimal_value_to_str(cancel_pulse_bw)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:CPBWidth {param}')

	def get_iterations(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ITERations \n
		Snippet: value: int = driver.source.bb.nr5G.output.cfReduction.get_iterations() \n
		Sets the number of iterations that are used for calculating the resulting crest factor. The iteration process is stopped
		when the desired crest factor is achieved by 0.1 dB. \n
			:return: max_iteration: integer Range: 0 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ITERations?')
		return Conversions.str_to_int(response)

	def set_iterations(self, max_iteration: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ITERations \n
		Snippet: driver.source.bb.nr5G.output.cfReduction.set_iterations(max_iteration = 1) \n
		Sets the number of iterations that are used for calculating the resulting crest factor. The iteration process is stopped
		when the desired crest factor is achieved by 0.1 dB. \n
			:param max_iteration: integer Range: 0 to 20
		"""
		param = Conversions.decimal_value_to_str(max_iteration)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ITERations {param}')

	def get_oc_factor(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:OCFactor \n
		Snippet: value: int = driver.source.bb.nr5G.output.cfReduction.get_oc_factor() \n
		Queries the original crest factor of the waveform after the calculation of the resulting crest factor is completed. The
		original crest factor is calculated as an average over the whole waveform, including any idle periods that might be
		present in TDD waveforms. \n
			:return: original_cfr: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:OCFactor?')
		return Conversions.str_to_int(response)

	def get_rc_factor(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:RCFactor \n
		Snippet: value: int = driver.source.bb.nr5G.output.cfReduction.get_rc_factor() \n
		Queries the resulting crest factor of the waveform after the calculations are completed. The resulting crest factor is
		calculated as an average over the whole waveform, including any idle periods that might be present in TDD waveforms. \n
			:return: resulting_cfr: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:RCFactor?')
		return Conversions.str_to_int(response)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:STATe \n
		Snippet: value: bool = driver.source.bb.nr5G.output.cfReduction.get_state() \n
		Enables the crest factor reduction calculation. \n
			:return: crest_factor_stat: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, crest_factor_stat: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:STATe \n
		Snippet: driver.source.bb.nr5G.output.cfReduction.set_state(crest_factor_stat = False) \n
		Enables the crest factor reduction calculation. \n
			:param crest_factor_stat: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(crest_factor_stat)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:STATe {param}')

	def get_tcr_factor(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:TCRFactor \n
		Snippet: value: float = driver.source.bb.nr5G.output.cfReduction.get_tcr_factor() \n
		Sets the desired crest factor value. \n
			:return: target_crf: float Range: 0 to 30
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:TCRFactor?')
		return Conversions.str_to_float(response)

	def set_tcr_factor(self, target_crf: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:TCRFactor \n
		Snippet: driver.source.bb.nr5G.output.cfReduction.set_tcr_factor(target_crf = 1.0) \n
		Sets the desired crest factor value. \n
			:param target_crf: float Range: 0 to 30
		"""
		param = Conversions.decimal_value_to_str(target_crf)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:TCRFactor {param}')

	def get_tr_bwidth(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:TRBWidth \n
		Snippet: value: float = driver.source.bb.nr5G.output.cfReduction.get_tr_bwidth() \n
		Sets the transition bandwidth of the cancellation pulse.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:OUTPut:CFReduction:ALGorithm = PC \n
			:return: transit_bw: float Range: 0 to 500e6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:TRBWidth?')
		return Conversions.str_to_float(response)

	def set_tr_bwidth(self, transit_bw: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:TRBWidth \n
		Snippet: driver.source.bb.nr5G.output.cfReduction.set_tr_bwidth(transit_bw = 1.0) \n
		Sets the transition bandwidth of the cancellation pulse.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:OUTPut:CFReduction:ALGorithm = PC \n
			:param transit_bw: float Range: 0 to 500e6
		"""
		param = Conversions.decimal_value_to_str(transit_bw)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:TRBWidth {param}')
