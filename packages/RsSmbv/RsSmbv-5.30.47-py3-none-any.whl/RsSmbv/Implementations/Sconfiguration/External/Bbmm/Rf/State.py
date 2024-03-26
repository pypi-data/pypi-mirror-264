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

	def set(self, rem_conn_state: bool, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:RF:STATe \n
		Snippet: driver.sconfiguration.external.bbmm.rf.state.set(rem_conn_state = False, iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param rem_conn_state: No help available
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = Conversions.bool_to_str(rem_conn_state)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:RF:STATe {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:RF:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.bbmm.rf.state.get(iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
			:return: rem_conn_state: No help available"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:RF:STATe?')
		return Conversions.str_to_bool(response)
