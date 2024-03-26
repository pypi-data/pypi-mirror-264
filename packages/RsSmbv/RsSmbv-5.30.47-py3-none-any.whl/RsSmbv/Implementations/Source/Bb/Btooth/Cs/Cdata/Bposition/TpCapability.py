from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpCapabilityCls:
	"""TpCapability commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpCapability", core, parent)

	def set(self, tpm_capability: bool, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[BPOSition<CH0>]:TPCapability \n
		Snippet: driver.source.bb.btooth.cs.cdata.bposition.tpCapability.set(tpm_capability = False, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param tpm_capability: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bposition')
		"""
		param = Conversions.bool_to_str(tpm_capability)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:BPOSition{channelNull_cmd_val}:TPCapability {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[BPOSition<CH0>]:TPCapability \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.bposition.tpCapability.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bposition')
			:return: tpm_capability: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:BPOSition{channelNull_cmd_val}:TPCapability?')
		return Conversions.str_to_bool(response)
