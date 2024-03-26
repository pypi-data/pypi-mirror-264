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

	def set(self, filename: str, digitalIq=repcap.DigitalIq.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:REMote:INITialization:PREDefined:FILE \n
		Snippet: driver.sconfiguration.external.fader.remote.initialization.predefined.file.set(filename = 'abc', digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param filename: No help available
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
		"""
		param = Conversions.value_to_quoted_str(filename)
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		self._core.io.write(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:REMote:INITialization:PREDefined:FILE {param}')
