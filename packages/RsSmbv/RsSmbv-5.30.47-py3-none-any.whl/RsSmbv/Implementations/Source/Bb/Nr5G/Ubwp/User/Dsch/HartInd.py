from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HartIndCls:
	"""HartInd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hartInd", core, parent)

	def set(self, harq_ack_retrans_i: bool, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:DSCH:HARTind \n
		Snippet: driver.source.bb.nr5G.ubwp.user.dsch.hartInd.set(harq_ack_retrans_i = False, userNull = repcap.UserNull.Default) \n
		Turns the 'HARQ-ACK Retransmission Indicator' field available in DCI format 1_1 on and off. \n
			:param harq_ack_retrans_i: 1| ON| 0| OFF
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(harq_ack_retrans_i)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:DSCH:HARTind {param}')

	def get(self, userNull=repcap.UserNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:DSCH:HARTind \n
		Snippet: value: bool = driver.source.bb.nr5G.ubwp.user.dsch.hartInd.get(userNull = repcap.UserNull.Default) \n
		Turns the 'HARQ-ACK Retransmission Indicator' field available in DCI format 1_1 on and off. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: harq_ack_retrans_i: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:DSCH:HARTind?')
		return Conversions.str_to_bool(response)
