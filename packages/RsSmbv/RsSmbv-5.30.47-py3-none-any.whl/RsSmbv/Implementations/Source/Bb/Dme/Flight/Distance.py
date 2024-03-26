from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DistanceCls:
	"""Distance commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("distance", core, parent)

	def get_current(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:DISTance:CURRent \n
		Snippet: value: float = driver.source.bb.dme.flight.distance.get_current() \n
		Queires the current distance of the aircraft in the flight simulation. \n
			:return: current_distance: float Range: -400 to 400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FLIGht:DISTance:CURRent?')
		return Conversions.str_to_float(response)

	def get_start(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:DISTance:STARt \n
		Snippet: value: float = driver.source.bb.dme.flight.distance.get_start() \n
		Sets the start distance of the flight simulation. \n
			:return: start_distance: float Range: -400 to 400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FLIGht:DISTance:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start_distance: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:DISTance:STARt \n
		Snippet: driver.source.bb.dme.flight.distance.set_start(start_distance = 1.0) \n
		Sets the start distance of the flight simulation. \n
			:param start_distance: float Range: -400 to 400
		"""
		param = Conversions.decimal_value_to_str(start_distance)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FLIGht:DISTance:STARt {param}')

	def get_stop(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:DISTance:STOP \n
		Snippet: value: float = driver.source.bb.dme.flight.distance.get_stop() \n
		Sets the stop distance of the flight simulation. \n
			:return: stop_distance: float Range: -400 to 400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FLIGht:DISTance:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop_distance: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:DISTance:STOP \n
		Snippet: driver.source.bb.dme.flight.distance.set_stop(stop_distance = 1.0) \n
		Sets the stop distance of the flight simulation. \n
			:param stop_distance: float Range: -400 to 400
		"""
		param = Conversions.decimal_value_to_str(stop_distance)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FLIGht:DISTance:STOP {param}')
