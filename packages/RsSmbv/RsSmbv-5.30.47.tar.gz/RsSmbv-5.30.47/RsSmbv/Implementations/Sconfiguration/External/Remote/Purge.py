from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PurgeCls:
	"""Purge commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("purge", core, parent)

	def set(self) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:PURGe \n
		Snippet: driver.sconfiguration.external.remote.purge.set() \n
		Removes unused instruments from the pool of external instruments. \n
		"""
		self._core.io.write(f'SCONfiguration:EXTernal:REMote:PURGe')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:PURGe \n
		Snippet: driver.sconfiguration.external.remote.purge.set_with_opc() \n
		Removes unused instruments from the pool of external instruments. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:EXTernal:REMote:PURGe', opc_timeout_ms)
