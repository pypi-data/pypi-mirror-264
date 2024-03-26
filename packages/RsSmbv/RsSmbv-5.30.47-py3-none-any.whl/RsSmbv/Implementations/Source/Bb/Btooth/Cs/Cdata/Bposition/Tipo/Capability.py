from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CapabilityCls:
	"""Capability commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("capability", core, parent)

	def set(self, tio_capability: bool, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[BPOSition<CH0>]:TIPO:CAPability \n
		Snippet: driver.source.bb.btooth.cs.cdata.bposition.tipo.capability.set(tio_capability = False, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param tio_capability: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bposition')
		"""
		param = Conversions.bool_to_str(tio_capability)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:BPOSition{channelNull_cmd_val}:TIPO:CAPability {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[BPOSition<CH0>]:TIPO:CAPability \n
		Snippet: value: bool = driver.source.bb.btooth.cs.cdata.bposition.tipo.capability.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bposition')
			:return: tio_capability: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:BPOSition{channelNull_cmd_val}:TIPO:CAPability?')
		return Conversions.str_to_bool(response)
