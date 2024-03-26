from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoveCls:
	"""Remove commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("remove", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:REMove \n
		Snippet: driver.source.areGenerator.external.remote.edit.remove.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:REMove')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:REMove \n
		Snippet: driver.source.areGenerator.external.remote.edit.remove.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:REMove', opc_timeout_ms)
