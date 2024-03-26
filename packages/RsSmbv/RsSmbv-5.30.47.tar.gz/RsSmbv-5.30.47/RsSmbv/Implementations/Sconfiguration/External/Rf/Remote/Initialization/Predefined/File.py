from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def set(self, filename: str, path=repcap.Path.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:REMote:INITialization:PREDefined:FILE \n
		Snippet: driver.sconfiguration.external.rf.remote.initialization.predefined.file.set(filename = 'abc', path = repcap.Path.Default) \n
		No command help available \n
			:param filename: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = Conversions.value_to_quoted_str(filename)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SCONfiguration:EXTernal:RF{path_cmd_val}:REMote:INITialization:PREDefined:FILE {param}')
