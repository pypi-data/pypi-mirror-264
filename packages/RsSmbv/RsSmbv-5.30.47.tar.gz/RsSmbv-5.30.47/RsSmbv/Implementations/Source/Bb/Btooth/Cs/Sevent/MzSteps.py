from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MzStepsCls:
	"""MzSteps commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mzSteps", core, parent)

	def set(self, mode_0_steps: int, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MZSTeps \n
		Snippet: driver.source.bb.btooth.cs.sevent.mzSteps.set(mode_0_steps = 1, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param mode_0_steps: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.decimal_value_to_str(mode_0_steps)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MZSTeps {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MZSTeps \n
		Snippet: value: int = driver.source.bb.btooth.cs.sevent.mzSteps.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: mode_0_steps: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MZSTeps?')
		return Conversions.str_to_int(response)
