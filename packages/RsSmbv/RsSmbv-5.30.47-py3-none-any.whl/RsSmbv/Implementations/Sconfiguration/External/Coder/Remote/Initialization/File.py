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
		"""SCPI: SCONfiguration:EXTernal:CODer<CH>:REMote:INITialization:FILE \n
		Snippet: driver.sconfiguration.external.coder.remote.initialization.file.set(filename = 'abc', index = repcap.Index.Default) \n
		No command help available \n
			:param filename: No help available
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coder')
		"""
		param = Conversions.value_to_quoted_str(filename)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:CODer{index_cmd_val}:REMote:INITialization:FILE {param}')

	def get(self, index=repcap.Index.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:CODer<CH>:REMote:INITialization:FILE \n
		Snippet: value: str = driver.sconfiguration.external.coder.remote.initialization.file.get(index = repcap.Index.Default) \n
		No command help available \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coder')
			:return: filename: No help available"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:CODer{index_cmd_val}:REMote:INITialization:FILE?')
		return trim_str_response(response)
