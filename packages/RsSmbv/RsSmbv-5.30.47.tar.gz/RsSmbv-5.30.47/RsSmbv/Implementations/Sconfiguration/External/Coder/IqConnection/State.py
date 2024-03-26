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

	def get(self, index=repcap.Index.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:CODer<CH>:IQConnection:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.coder.iqConnection.state.get(index = repcap.Index.Default) \n
		No command help available \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Coder')
			:return: ipart_qconn_state: No help available"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:CODer{index_cmd_val}:IQConnection:STATe?')
		return Conversions.str_to_bool(response)
