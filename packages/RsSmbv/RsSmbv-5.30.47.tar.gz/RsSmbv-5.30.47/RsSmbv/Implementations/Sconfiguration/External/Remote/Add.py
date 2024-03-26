from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AddCls:
	"""Add commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("add", core, parent)

	def set(self, instr_name: List[str], hw_chan: str, tcp_ipor_usb_addr: str, rf_path_number: str = None) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:ADD \n
		Snippet: driver.sconfiguration.external.remote.add.set(instr_name = ['abc1', 'abc2', 'abc3'], hw_chan = 'abc', tcp_ipor_usb_addr = 'abc', rf_path_number = 'abc') \n
		Adds manually an external instrument to the list of available instruments. \n
			:param instr_name: String Alias name of the instrument
			:param hw_chan: String Hardware channel (USB or LAN) used by the remote channel to the external instrument Range: 'LAN' to 'USB'
			:param tcp_ipor_usb_addr: String IP address or hostname of the connected external instrument
			:param rf_path_number: String Determines the number of RF paths the external instrument is equipped with Range: '1' to '2'
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('instr_name', instr_name, DataType.StringList, None), ArgSingle('hw_chan', hw_chan, DataType.String), ArgSingle('tcp_ipor_usb_addr', tcp_ipor_usb_addr, DataType.String), ArgSingle('rf_path_number', rf_path_number, DataType.String, None, is_optional=True))
		self._core.io.write(f'SCONfiguration:EXTernal:REMote:ADD {param}'.rstrip())
