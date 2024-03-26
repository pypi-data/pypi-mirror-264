from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, rem_conn_state: bool, digitalIq=repcap.DigitalIq.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:RF:STATe \n
		Snippet: driver.sconfiguration.external.fader.rf.state.set(rem_conn_state = False, digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param rem_conn_state: No help available
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
		"""
		param = Conversions.bool_to_str(rem_conn_state)
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		self._core.io.write(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:RF:STATe {param}')

	def get(self, digitalIq=repcap.DigitalIq.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:RF:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.fader.rf.state.get(digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: rem_conn_state: No help available"""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:RF:STATe?')
		return Conversions.str_to_bool(response)
