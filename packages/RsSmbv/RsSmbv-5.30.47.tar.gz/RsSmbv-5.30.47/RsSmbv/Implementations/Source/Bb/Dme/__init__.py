from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmeCls:
	"""Dme commands group definition. 91 total commands, 14 Subgroups, 14 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dme", core, parent)

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def ppst(self):
		"""ppst commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ppst'):
			from .Ppst import PpstCls
			self._ppst = PpstCls(self._core, self._cmd_group)
		return self._ppst

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def analysis(self):
		"""analysis commands group. 1 Sub-classes, 11 commands."""
		if not hasattr(self, '_analysis'):
			from .Analysis import AnalysisCls
			self._analysis = AnalysisCls(self._core, self._cmd_group)
		return self._analysis

	@property
	def echo(self):
		"""echo commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_echo'):
			from .Echo import EchoCls
			self._echo = EchoCls(self._core, self._cmd_group)
		return self._echo

	@property
	def efficiency(self):
		"""efficiency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_efficiency'):
			from .Efficiency import EfficiencyCls
			self._efficiency = EfficiencyCls(self._core, self._cmd_group)
		return self._efficiency

	@property
	def flight(self):
		"""flight commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_flight'):
			from .Flight import FlightCls
			self._flight = FlightCls(self._core, self._cmd_group)
		return self._flight

	@property
	def gaussian(self):
		"""gaussian commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gaussian'):
			from .Gaussian import GaussianCls
			self._gaussian = GaussianCls(self._core, self._cmd_group)
		return self._gaussian

	@property
	def icao(self):
		"""icao commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icao'):
			from .Icao import IcaoCls
			self._icao = IcaoCls(self._core, self._cmd_group)
		return self._icao

	@property
	def id(self):
		"""id commands group. 2 Sub-classes, 11 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def marker(self):
		"""marker commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def pinput(self):
		"""pinput commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pinput'):
			from .Pinput import PinputCls
			self._pinput = PinputCls(self._core, self._cmd_group)
		return self._pinput

	@property
	def rdistance(self):
		"""rdistance commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rdistance'):
			from .Rdistance import RdistanceCls
			self._rdistance = RdistanceCls(self._core, self._cmd_group)
		return self._rdistance

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:DME:PRESet \n
		Snippet: driver.source.bb.dme.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:DME:PRESet \n
		Snippet: driver.source.bb.dme.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DME:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DME:STATe \n
		Snippet: value: bool = driver.source.bb.dme.get_state() \n
		Activates/deactivates the avionic standard. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DME:STATe \n
		Snippet: driver.source.bb.dme.set_state(state = False) \n
		Activates/deactivates the avionic standard. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:STATe {param}')

	# noinspection PyTypeChecker
	def get_csuffix(self) -> enums.AvionicDmeChanSuff:
		"""SCPI: [SOURce<HW>]:[BB]:DME:CSUFfix \n
		Snippet: value: enums.AvionicDmeChanSuff = driver.source.bb.dme.get_csuffix() \n
		Sets the channel that is simulated. Standard compliant X and Y channels differ in the spacing between the two pulses of
		the pulse pair and the delay of the ground station. \n
			:return: csuffix: X| Y| ICAO
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:CSUFfix?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmeChanSuff)

	def set_csuffix(self, csuffix: enums.AvionicDmeChanSuff) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:CSUFfix \n
		Snippet: driver.source.bb.dme.set_csuffix(csuffix = enums.AvionicDmeChanSuff.ICAO) \n
		Sets the channel that is simulated. Standard compliant X and Y channels differ in the spacing between the two pulses of
		the pulse pair and the delay of the ground station. \n
			:param csuffix: X| Y| ICAO
		"""
		param = Conversions.enum_scalar_to_str(csuffix, enums.AvionicDmeChanSuff)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:CSUFfix {param}')

	def get_fall(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FALL \n
		Snippet: value: float = driver.source.bb.dme.get_fall() \n
		Sets the fall time of the pulse (90% to 10% of peak voltage) . \n
			:return: fall: float Range: 0.5E-6 to 10E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FALL?')
		return Conversions.str_to_float(response)

	def set_fall(self, fall: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FALL \n
		Snippet: driver.source.bb.dme.set_fall(fall = 1.0) \n
		Sets the fall time of the pulse (90% to 10% of peak voltage) . \n
			:param fall: float Range: 0.5E-6 to 10E-6
		"""
		param = Conversions.decimal_value_to_str(fall)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FALL {param}')

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FREQuency \n
		Snippet: value: float = driver.source.bb.dme.get_frequency() \n
		Sets the carrier frequency of the signal. \n
			:return: carrier_freq: float Range: 100E3 to 6E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, carrier_freq: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FREQuency \n
		Snippet: driver.source.bb.dme.set_frequency(carrier_freq = 1.0) \n
		Sets the carrier frequency of the signal. \n
			:param carrier_freq: float Range: 100E3 to 6E9
		"""
		param = Conversions.decimal_value_to_str(carrier_freq)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FREQuency {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicDmeMode:
		"""SCPI: [SOURce<HW>]:[BB]:DME:MODE \n
		Snippet: value: enums.AvionicDmeMode = driver.source.bb.dme.get_mode() \n
		Selects the mode of the DME modulation. The mode determines the signal type that is simulated. The exact timing of the
		signal for each mode is determined by the channel selected with[:SOURce<hw>][:BB]:DME:CSUFfix. \n
			:return: mode: INTerrogation| REPLy INTerrogation The interrogation signal of the airborne transmitter is simulated. REPLy The reply signal of the ground based transponder is simulated. The trigger is automatically set to external and the default trigger delay either to 50 us (channel X) or 56 us (channel Y) depending on the selected channel ([:SOURcehw][:BB]:DME:CSUFfix) . The interval between the pulse pairs can be set to a fixed value (repetition rate, [:SOURcehw][:BB]:DME:RATE) or to random generation (pulse squitter, [:SOURcehw][:BB]:DME:SQUitter) . The trigger signal is input via the Pulse Ext connector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmeMode)

	def set_mode(self, mode: enums.AvionicDmeMode) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:MODE \n
		Snippet: driver.source.bb.dme.set_mode(mode = enums.AvionicDmeMode.INTerrogation) \n
		Selects the mode of the DME modulation. The mode determines the signal type that is simulated. The exact timing of the
		signal for each mode is determined by the channel selected with[:SOURce<hw>][:BB]:DME:CSUFfix. \n
			:param mode: INTerrogation| REPLy INTerrogation The interrogation signal of the airborne transmitter is simulated. REPLy The reply signal of the ground based transponder is simulated. The trigger is automatically set to external and the default trigger delay either to 50 us (channel X) or 56 us (channel Y) depending on the selected channel ([:SOURcehw][:BB]:DME:CSUFfix) . The interval between the pulse pairs can be set to a fixed value (repetition rate, [:SOURcehw][:BB]:DME:RATE) or to random generation (pulse squitter, [:SOURcehw][:BB]:DME:SQUitter) . The trigger signal is input via the Pulse Ext connector.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicDmeMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:MODE {param}')

	def get_pps(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:PPS \n
		Snippet: value: float = driver.source.bb.dme.get_pps() \n
		Sets the spacing between the first and second pulse of a pulse pair (time between halfvoltage points on the leading edge
		of each pulse) . Available only for [:SOURce<hw>][:BB]:DME:SINGleOFF \n
			:return: pps: float Range: 1E-6 to 200E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PPS?')
		return Conversions.str_to_float(response)

	def set_pps(self, pps: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:PPS \n
		Snippet: driver.source.bb.dme.set_pps(pps = 1.0) \n
		Sets the spacing between the first and second pulse of a pulse pair (time between halfvoltage points on the leading edge
		of each pulse) . Available only for [:SOURce<hw>][:BB]:DME:SINGleOFF \n
			:param pps: float Range: 1E-6 to 200E-6
		"""
		param = Conversions.decimal_value_to_str(pps)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PPS {param}')

	def get_rate(self) -> int:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RATE \n
		Snippet: value: int = driver.source.bb.dme.get_rate() \n
		If [:SOURce<hw>][:BB]:DME:MODE is set to INTerrogation, sets the pulse repetition rate. If [:SOURce<hw>][:BB]:DME:MODE is
		set to REPLy, indicates the mean pulse repetition rate in squitter mode. \n
			:return: rate: integer Range: 10 to 6000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RATE?')
		return Conversions.str_to_int(response)

	def set_rate(self, rate: int) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RATE \n
		Snippet: driver.source.bb.dme.set_rate(rate = 1) \n
		If [:SOURce<hw>][:BB]:DME:MODE is set to INTerrogation, sets the pulse repetition rate. If [:SOURce<hw>][:BB]:DME:MODE is
		set to REPLy, indicates the mean pulse repetition rate in squitter mode. \n
			:param rate: integer Range: 10 to 6000
		"""
		param = Conversions.decimal_value_to_str(rate)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RATE {param}')

	def get_rise(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RISE \n
		Snippet: value: float = driver.source.bb.dme.get_rise() \n
		Sets the rise time of the pulse (10% to 90% of peak voltage) . \n
			:return: rise: float Range: 0.5E-6 to 10E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RISE?')
		return Conversions.str_to_float(response)

	def set_rise(self, rise: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RISE \n
		Snippet: driver.source.bb.dme.set_rise(rise = 1.0) \n
		Sets the rise time of the pulse (10% to 90% of peak voltage) . \n
			:param rise: float Range: 0.5E-6 to 10E-6
		"""
		param = Conversions.decimal_value_to_str(rise)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RISE {param}')

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.AvionicDmePulsShap:
		"""SCPI: [SOURce<HW>]:[BB]:DME:SHAPe \n
		Snippet: value: enums.AvionicDmePulsShap = driver.source.bb.dme.get_shape() \n
		Sets the pulse shape. \n
			:return: shape: COS2| LIN| COS| GAUSs COS2| The rising edge is cos shaped and the falling edge is cos^2 shaped. LIN The falling and the rising edge of the pulse are shaped linear. COS The falling and the rising edge of the pulse are cos^2 shaped.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmePulsShap)

	def set_shape(self, shape: enums.AvionicDmePulsShap) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:SHAPe \n
		Snippet: driver.source.bb.dme.set_shape(shape = enums.AvionicDmePulsShap.COS) \n
		Sets the pulse shape. \n
			:param shape: COS2| LIN| COS| GAUSs COS2| The rising edge is cos shaped and the falling edge is cos^2 shaped. LIN The falling and the rising edge of the pulse are shaped linear. COS The falling and the rising edge of the pulse are cos^2 shaped.
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.AvionicDmePulsShap)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SHAPe {param}')

	def get_single(self) -> bool:
		"""SCPI: [SOURce<HW>]:[BB]:DME:SINGle \n
		Snippet: value: bool = driver.source.bb.dme.get_single() \n
		Activates/deactivates generation of a single test pulse. \n
			:return: single: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:SINGle?')
		return Conversions.str_to_bool(response)

	def set_single(self, single: bool) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:SINGle \n
		Snippet: driver.source.bb.dme.set_single(single = False) \n
		Activates/deactivates generation of a single test pulse. \n
			:param single: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(single)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SINGle {param}')

	def get_squitter(self) -> bool:
		"""SCPI: [SOURce<HW>]:[BB]:DME:SQUitter \n
		Snippet: value: bool = driver.source.bb.dme.get_squitter() \n
		Activates/deactivates the random pulse repetition rate. The average repetition rate is 2700 pp/s. The pulse spacing is
		distributed randomly in the range of 60 us to about 1500 us according to EUROCAE EN-54 6.2.12. The squitter pulses are
		constantly sent by the ground station in order to ensure proper operation and in order to ease synchronization of the
		aircraft interrogator to the ground station. \n
			:return: squitter: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:SQUitter?')
		return Conversions.str_to_bool(response)

	def set_squitter(self, squitter: bool) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:SQUitter \n
		Snippet: driver.source.bb.dme.set_squitter(squitter = False) \n
		Activates/deactivates the random pulse repetition rate. The average repetition rate is 2700 pp/s. The pulse spacing is
		distributed randomly in the range of 60 us to about 1500 us according to EUROCAE EN-54 6.2.12. The squitter pulses are
		constantly sent by the ground station in order to ensure proper operation and in order to ease synchronization of the
		aircraft interrogator to the ground station. \n
			:param squitter: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(squitter)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SQUitter {param}')

	def get_velocity(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:VELocity \n
		Snippet: value: float = driver.source.bb.dme.get_velocity() \n
		Sets the delay between the DME echo pulse signal and the original DME pulse signal. \n
			:return: dme_velocity: float Range: -1E4 to 1E4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:VELocity?')
		return Conversions.str_to_float(response)

	def set_velocity(self, dme_velocity: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:VELocity \n
		Snippet: driver.source.bb.dme.set_velocity(dme_velocity = 1.0) \n
		Sets the delay between the DME echo pulse signal and the original DME pulse signal. \n
			:param dme_velocity: float Range: -1E4 to 1E4
		"""
		param = Conversions.decimal_value_to_str(dme_velocity)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:VELocity {param}')

	def get_width(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:WIDTh \n
		Snippet: value: float = driver.source.bb.dme.get_width() \n
		Sets the pulse width (50% to 50% of peak voltage) . \n
			:return: width: float Range: 1E-6 to 100E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:WIDTh?')
		return Conversions.str_to_float(response)

	def set_width(self, width: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:WIDTh \n
		Snippet: driver.source.bb.dme.set_width(width = 1.0) \n
		Sets the pulse width (50% to 50% of peak voltage) . \n
			:param width: float Range: 1E-6 to 100E-6
		"""
		param = Conversions.decimal_value_to_str(width)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:WIDTh {param}')

	def clone(self) -> 'DmeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
