from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScanCls:
	"""Scan commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scan", core, parent)

	def set(self) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:SCAN \n
		Snippet: driver.sconfiguration.external.remote.scan.set() \n
		Scans the network for connected instruments. \n
		"""
		self._core.io.write(f'SCONfiguration:EXTernal:REMote:SCAN')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:SCAN \n
		Snippet: driver.sconfiguration.external.remote.scan.set_with_opc() \n
		Scans the network for connected instruments. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:EXTernal:REMote:SCAN', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: SCONfiguration:EXTernal:REMote:SCAN:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.remote.scan.get_state() \n
		Queries if scanning is performed or not. To start the scanning process, use the command method RsSmbv.Sconfiguration.
		External.Remote.Scan.set. \n
			:return: scan_state: 1| ON| 0| OFF 1 Scanning process running 0 Not scanning
		"""
		response = self._core.io.query_str('SCONfiguration:EXTernal:REMote:SCAN:STATe?')
		return Conversions.str_to_bool(response)
