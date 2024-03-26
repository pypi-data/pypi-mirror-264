from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TrajectoryCls:
	"""Trajectory commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trajectory", core, parent)

	def export(self, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:TRAJectory:EXPort \n
		Snippet: driver.source.bb.gnss.receiver.v.trajectory.export(vehicle = repcap.Vehicle.Default) \n
		No command help available \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
		"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:TRAJectory:EXPort')

	def export_with_opc(self, vehicle=repcap.Vehicle.Default, opc_timeout_ms: int = -1) -> None:
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:TRAJectory:EXPort \n
		Snippet: driver.source.bb.gnss.receiver.v.trajectory.export_with_opc(vehicle = repcap.Vehicle.Default) \n
		No command help available \n
		Same as export, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:TRAJectory:EXPort', opc_timeout_ms)
