from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CindexCls:
	"""Cindex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cindex", core, parent)

	def set(self, channel_index: int, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CINDex \n
		Snippet: driver.source.bb.btooth.cs.sevent.step.cindex.set(channel_index = 1, channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param channel_index: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = Conversions.decimal_value_to_str(channel_index)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CINDex {param}')

	def get(self, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CINDex \n
		Snippet: value: int = driver.source.bb.btooth.cs.sevent.step.cindex.get(channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: channel_index: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CINDex?')
		return Conversions.str_to_int(response)
