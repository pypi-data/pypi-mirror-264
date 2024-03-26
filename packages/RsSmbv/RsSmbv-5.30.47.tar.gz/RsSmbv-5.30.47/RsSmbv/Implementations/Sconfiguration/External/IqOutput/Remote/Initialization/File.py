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

	def set(self, filename: str, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:INITialization:FILE \n
		Snippet: driver.sconfiguration.external.iqOutput.remote.initialization.file.set(filename = 'abc', iqConnector = repcap.IqConnector.Default) \n
		Queries the currently selected initialization file. \n
			:param filename: string filename with file extension (*.iec)
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		param = Conversions.value_to_quoted_str(filename)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:INITialization:FILE {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:INITialization:FILE \n
		Snippet: value: str = driver.sconfiguration.external.iqOutput.remote.initialization.file.get(iqConnector = repcap.IqConnector.Default) \n
		Queries the currently selected initialization file. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: filename: string filename with file extension (*.iec)"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:INITialization:FILE?')
		return trim_str_response(response)
