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

	def set(self, rem_conn_state: bool, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:RF:STATe \n
		Snippet: driver.sconfiguration.external.hsDigital.rf.state.set(rem_conn_state = False, index = repcap.Index.Default) \n
		Queries/sets the RF output state of the connected external instrument. \n
			:param rem_conn_state: 1| ON| 0| OFF
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
		"""
		param = Conversions.bool_to_str(rem_conn_state)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:RF:STATe {param}')

	def get(self, index=repcap.Index.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:RF:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.hsDigital.rf.state.get(index = repcap.Index.Default) \n
		Queries/sets the RF output state of the connected external instrument. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
			:return: rem_conn_state: 1| ON| 0| OFF"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:RF:STATe?')
		return Conversions.str_to_bool(response)
