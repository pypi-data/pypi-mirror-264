from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpcCls:
	"""Spc commands group definition. 10 total commands, 2 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spc", core, parent)

	@property
	def measure(self):
		"""measure commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_measure'):
			from .Measure import MeasureCls
			self._measure = MeasureCls(self._core, self._cmd_group)
		return self._measure

	@property
	def single(self):
		"""single commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_single'):
			from .Single import SingleCls
			self._single = SingleCls(self._core, self._cmd_group)
		return self._single

	def get_crange(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:SPC:CRANge \n
		Snippet: value: float = driver.source.power.spc.get_crange() \n
		Defines the capture range of the power control system. Within the range: Target Level +/- Catch Range the power control
		locks and tries to achieve the target level. Readings outside the range are not considered. \n
			:return: pow_cntrl_crange: float Range: 0 to 50
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:CRANge?')
		return Conversions.str_to_float(response)

	def set_crange(self, pow_cntrl_crange: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:CRANge \n
		Snippet: driver.source.power.spc.set_crange(pow_cntrl_crange = 1.0) \n
		Defines the capture range of the power control system. Within the range: Target Level +/- Catch Range the power control
		locks and tries to achieve the target level. Readings outside the range are not considered. \n
			:param pow_cntrl_crange: float Range: 0 to 50
		"""
		param = Conversions.decimal_value_to_str(pow_cntrl_crange)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:CRANge {param}')

	def get_delay(self) -> int:
		"""SCPI: [SOURce<HW>]:POWer:SPC:DELay \n
		Snippet: value: int = driver.source.power.spc.get_delay() \n
		Sets a waiting time for the generator to adjust the output level. After the delay time has elapsed, the power sensor
		measures the next value. \n
			:return: pow_cntrl_delay: integer Range: 0 to 1000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:DELay?')
		return Conversions.str_to_int(response)

	def set_delay(self, pow_cntrl_delay: int) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:DELay \n
		Snippet: driver.source.power.spc.set_delay(pow_cntrl_delay = 1) \n
		Sets a waiting time for the generator to adjust the output level. After the delay time has elapsed, the power sensor
		measures the next value. \n
			:param pow_cntrl_delay: integer Range: 0 to 1000
		"""
		param = Conversions.decimal_value_to_str(pow_cntrl_delay)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:DELay {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SensorModeAll:
		"""SCPI: [SOURce<HW>]:POWer:SPC:MODE \n
		Snippet: value: enums.SensorModeAll = driver.source.power.spc.get_mode() \n
		Selects the measurement mode for the power sensor. \n
			:return: control_mode: AUTO| SINGle AUTO Measures the level values continuously. SINGle Executes one measurement, triggered by the command [:SOURcehw]:POWer:SPC:SINGle.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SensorModeAll)

	def set_mode(self, control_mode: enums.SensorModeAll) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:MODE \n
		Snippet: driver.source.power.spc.set_mode(control_mode = enums.SensorModeAll.AUTO) \n
		Selects the measurement mode for the power sensor. \n
			:param control_mode: AUTO| SINGle AUTO Measures the level values continuously. SINGle Executes one measurement, triggered by the command [:SOURcehw]:POWer:SPC:SINGle.
		"""
		param = Conversions.enum_scalar_to_str(control_mode, enums.SensorModeAll)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:MODE {param}')

	def get_peak(self) -> bool:
		"""SCPI: [SOURce<HW>]:POWer:SPC:PEAK \n
		Snippet: value: bool = driver.source.power.spc.get_peak() \n
		Activates power control by means of the peak power values, provided the power sensor supports this function. \n
			:return: pow_cntrl_peak: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:PEAK?')
		return Conversions.str_to_bool(response)

	def set_peak(self, pow_cntrl_peak: bool) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:PEAK \n
		Snippet: driver.source.power.spc.set_peak(pow_cntrl_peak = False) \n
		Activates power control by means of the peak power values, provided the power sensor supports this function. \n
			:param pow_cntrl_peak: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(pow_cntrl_peak)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:PEAK {param}')

	# noinspection PyTypeChecker
	def get_select(self) -> enums.PowCntrlSelect:
		"""SCPI: [SOURce<HW>]:POWer:SPC:SELect \n
		Snippet: value: enums.PowCntrlSelect = driver.source.power.spc.get_select() \n
		Selects the power sensor used for power control. \n
			:return: pow_cntrl_select: SENS1| SENS2| SENS3| SENS4| SENSor1| SENSor2| SENSor3| SENSor4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:SELect?')
		return Conversions.str_to_scalar_enum(response, enums.PowCntrlSelect)

	def set_select(self, pow_cntrl_select: enums.PowCntrlSelect) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:SELect \n
		Snippet: driver.source.power.spc.set_select(pow_cntrl_select = enums.PowCntrlSelect.SENS1) \n
		Selects the power sensor used for power control. \n
			:param pow_cntrl_select: SENS1| SENS2| SENS3| SENS4| SENSor1| SENSor2| SENSor3| SENSor4
		"""
		param = Conversions.enum_scalar_to_str(pow_cntrl_select, enums.PowCntrlSelect)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:SELect {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:POWer:SPC:STATe \n
		Snippet: value: bool = driver.source.power.spc.get_state() \n
		Starts power control using the selected sensor. The control loop periodically adjusts the output level of the signal
		generator. After switching off, the running loop is completed. \n
			:return: pow_cntrl_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, pow_cntrl_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:STATe \n
		Snippet: driver.source.power.spc.set_state(pow_cntrl_state = False) \n
		Starts power control using the selected sensor. The control loop periodically adjusts the output level of the signal
		generator. After switching off, the running loop is completed. \n
			:param pow_cntrl_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(pow_cntrl_state)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:STATe {param}')

	def get_target(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:SPC:TARGet \n
		Snippet: value: float = driver.source.power.spc.get_target() \n
		Sets the target level required at the DUT. To define the unit of the power value, use command method RsSmbv.Unit.power. \n
			:return: pow_cntrl_target: float Range: -50 to 30
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:TARGet?')
		return Conversions.str_to_float(response)

	def set_target(self, pow_cntrl_target: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:TARGet \n
		Snippet: driver.source.power.spc.set_target(pow_cntrl_target = 1.0) \n
		Sets the target level required at the DUT. To define the unit of the power value, use command method RsSmbv.Unit.power. \n
			:param pow_cntrl_target: float Range: -50 to 30
		"""
		param = Conversions.decimal_value_to_str(pow_cntrl_target)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:TARGet {param}')

	def get_warning_py(self) -> bool:
		"""SCPI: [SOURce<HW>]:POWer:SPC:WARNing \n
		Snippet: value: bool = driver.source.power.spc.get_warning_py() \n
		Queries if the activated power control works properly. If the power control does not work, the query returns warning
		state 1. On the screen, the R&S SMBV100B indicates a warning icon. \n
			:return: warning_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SPC:WARNing?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'SpcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
