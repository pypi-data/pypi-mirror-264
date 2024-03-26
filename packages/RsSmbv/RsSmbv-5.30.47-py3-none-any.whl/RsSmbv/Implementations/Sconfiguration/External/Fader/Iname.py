from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InameCls:
	"""Iname commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iname", core, parent)

	def get(self, digitalIq=repcap.DigitalIq.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:INAMe \n
		Snippet: value: str = driver.sconfiguration.external.fader.iname.get(digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: instr_name: No help available"""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:INAMe?')
		return trim_str_response(response)
