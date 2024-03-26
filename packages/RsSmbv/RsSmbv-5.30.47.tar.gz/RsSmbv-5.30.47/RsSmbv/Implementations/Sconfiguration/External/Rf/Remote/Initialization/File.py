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

	def set(self, filename: str, path=repcap.Path.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:REMote:INITialization:FILE \n
		Snippet: driver.sconfiguration.external.rf.remote.initialization.file.set(filename = 'abc', path = repcap.Path.Default) \n
		No command help available \n
			:param filename: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = Conversions.value_to_quoted_str(filename)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SCONfiguration:EXTernal:RF{path_cmd_val}:REMote:INITialization:FILE {param}')

	def get(self, path=repcap.Path.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:REMote:INITialization:FILE \n
		Snippet: value: str = driver.sconfiguration.external.rf.remote.initialization.file.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: filename: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:REMote:INITialization:FILE?')
		return trim_str_response(response)
