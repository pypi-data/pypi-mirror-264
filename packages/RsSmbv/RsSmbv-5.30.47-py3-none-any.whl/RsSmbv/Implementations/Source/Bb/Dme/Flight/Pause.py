from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PauseCls:
	"""Pause commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pause", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:PAUSe \n
		Snippet: driver.source.bb.dme.flight.pause.set() \n
		Pauses a running flight simulation. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FLIGht:PAUSe')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:FLIGht:PAUSe \n
		Snippet: driver.source.bb.dme.flight.pause.set_with_opc() \n
		Pauses a running flight simulation. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DME:FLIGht:PAUSe', opc_timeout_ms)
