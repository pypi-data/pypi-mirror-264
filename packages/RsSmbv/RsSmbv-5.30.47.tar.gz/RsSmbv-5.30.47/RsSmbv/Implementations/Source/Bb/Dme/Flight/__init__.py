from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FlightCls:
	"""Flight commands group definition. 10 total commands, 4 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("flight", core, parent)

	@property
	def distance(self):
		"""distance commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_distance'):
			from .Distance import DistanceCls
			self._distance = DistanceCls(self._core, self._cmd_group)
		return self._distance

	@property
	def pause(self):
		"""pause commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pause'):
			from .Pause import PauseCls
			self._pause = PauseCls(self._core, self._cmd_group)
		return self._pause

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restart'):
			from .Restart import RestartCls
			self._restart = RestartCls(self._core, self._cmd_group)
		return self._restart

	@property
	def resume(self):
		"""resume commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resume'):
			from .Resume import ResumeCls
			self._resume = ResumeCls(self._core, self._cmd_group)
		return self._resume

	# noinspection PyTypeChecker
	def get_rstatus(self) -> enums.AvionicDmeFlightStatus:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:RSTatus \n
		Snippet: value: enums.AvionicDmeFlightStatus = driver.source.bb.dme.flight.get_rstatus() \n
		Queries the status of the flight simulation. \n
			:return: running_status: OFF| IDLE| RUNNing| PAUSed
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FLIGht:RSTatus?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmeFlightStatus)

	def start(self) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:STARt \n
		Snippet: driver.source.bb.dme.flight.start() \n
		Starts the flight simulation with a given start distance. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FLIGht:STARt')

	def start_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:STARt \n
		Snippet: driver.source.bb.dme.flight.start_with_opc() \n
		Starts the flight simulation with a given start distance. \n
		Same as start, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DME:FLIGht:STARt', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:STATe \n
		Snippet: value: bool = driver.source.bb.dme.flight.get_state() \n
		Activates flight simulation. \n
			:return: sim_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FLIGht:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, sim_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:STATe \n
		Snippet: driver.source.bb.dme.flight.set_state(sim_state = False) \n
		Activates flight simulation. \n
			:param sim_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(sim_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FLIGht:STATe {param}')

	def stop(self) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:STOP \n
		Snippet: driver.source.bb.dme.flight.stop() \n
		Stops the flight simulation and sets the distance position to start distance. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FLIGht:STOP')

	def stop_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:STOP \n
		Snippet: driver.source.bb.dme.flight.stop_with_opc() \n
		Stops the flight simulation and sets the distance position to start distance. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DME:FLIGht:STOP', opc_timeout_ms)

	def clone(self) -> 'FlightCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FlightCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
