from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TfCapabilityCls:
	"""TfCapability commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tfCapability", core, parent)

	def set(self, tfcs_capability: bool, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[BPOSition<CH0>]:TFCapability \n
		Snippet: driver.source.bb.btooth.cs.cdata.bposition.tfCapability.set(tfcs_capability = False, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param tfcs_capability: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bposition')
		"""
		param = Conversions.bool_to_str(tfcs_capability)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:BPOSition{channelNull_cmd_val}:TFCapability {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[BPOSition<CH0>]:TFCapability \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.bposition.tfCapability.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bposition')
			:return: tfcs_capability: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:BPOSition{channelNull_cmd_val}:TFCapability?')
		return Conversions.str_to_bool(response)
