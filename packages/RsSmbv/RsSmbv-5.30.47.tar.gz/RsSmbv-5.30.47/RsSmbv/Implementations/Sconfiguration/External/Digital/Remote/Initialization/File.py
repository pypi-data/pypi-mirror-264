from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def set(self, filename: str, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:REMote:INITialization:FILE \n
		Snippet: driver.sconfiguration.external.digital.remote.initialization.file.set(filename = 'abc', index = repcap.Index.Default) \n
		Queries the currently selected initialization file. \n
			:param filename: string filename with file extension (*.iec)
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
		"""
		param = Conversions.value_to_quoted_str(filename)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:REMote:INITialization:FILE {param}')

	def get(self, index=repcap.Index.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:REMote:INITialization:FILE \n
		Snippet: value: str = driver.sconfiguration.external.digital.remote.initialization.file.get(index = repcap.Index.Default) \n
		Queries the currently selected initialization file. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:return: filename: string filename with file extension (*.iec)"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:REMote:INITialization:FILE?')
		return trim_str_response(response)
