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

	def set(self, filename: str, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:REMote:INITialization:USER:FILE \n
		Snippet: driver.sconfiguration.external.bbmm.remote.initialization.user.file.set(filename = 'abc', iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param filename: No help available
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = Conversions.value_to_quoted_str(filename)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:REMote:INITialization:USER:FILE {param}')
