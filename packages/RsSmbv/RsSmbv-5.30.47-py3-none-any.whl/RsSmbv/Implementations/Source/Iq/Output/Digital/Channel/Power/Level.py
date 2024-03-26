from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def get(self, channelNull=repcap.ChannelNull.Default) -> float:
		"""SCPI: [SOURce]:IQ:OUTPut:DIGital:CHANnel<ST0>:POWer:LEVel \n
		Snippet: value: float = driver.source.iq.output.digital.channel.power.level.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: bbout_hs_level: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:CHANnel{channelNull_cmd_val}:POWer:LEVel?')
		return Conversions.str_to_float(response)
