from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfaeCls:
	"""Cfae commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfae", core, parent)

	def set(self, ch_fae: int, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[CHANnel<CH0>]:CFAE \n
		Snippet: driver.source.bb.btooth.cs.cdata.channel.cfae.set(ch_fae = 1, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param ch_fae: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
		"""
		param = Conversions.decimal_value_to_str(ch_fae)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CHANnel{channelNull_cmd_val}:CFAE {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:[CHANnel<CH0>]:CFAE \n
		Snippet: value: int = driver.source.bb.btooth.cs.cdata.channel.cfae.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: ch_fae: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:CHANnel{channelNull_cmd_val}:CFAE?')
		return Conversions.str_to_int(response)
