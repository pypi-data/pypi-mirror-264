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

	def set(self, rem_conn_state: bool, path=repcap.Path.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:STATe \n
		Snippet: driver.sconfiguration.external.rf.rf.state.set(rem_conn_state = False, path = repcap.Path.Default) \n
		No command help available \n
			:param rem_conn_state: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = Conversions.bool_to_str(rem_conn_state)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:STATe {param}')

	def get(self, path=repcap.Path.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.rf.rf.state.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: rem_conn_state: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:STATe?')
		return Conversions.str_to_bool(response)
