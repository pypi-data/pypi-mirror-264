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
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:RF:STATe \n
		Snippet: driver.sconfiguration.external.iqOutput.rf.state.set(rem_conn_state = False, iqConnector = repcap.IqConnector.Default) \n
		Queries/sets the RF output state of the connected external instrument. \n
			:param rem_conn_state: 1| ON| 0| OFF
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		param = Conversions.bool_to_str(rem_conn_state)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:RF:STATe {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:RF:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.iqOutput.rf.state.get(iqConnector = repcap.IqConnector.Default) \n
		Queries/sets the RF output state of the connected external instrument. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: rem_conn_state: 1| ON| 0| OFF"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:RF:STATe?')
		return Conversions.str_to_bool(response)
