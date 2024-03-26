from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CtExtensionCls:
	"""CtExtension commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ctExtension", core, parent)

	def set(self, cs_tone_ext: bool, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CTEXtension \n
		Snippet: driver.source.bb.btooth.cs.sevent.step.ctExtension.set(cs_tone_ext = False, channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param cs_tone_ext: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = Conversions.bool_to_str(cs_tone_ext)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CTEXtension {param}')

	def get(self, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CTEXtension \n
		Snippet: value: bool = driver.source.bb.btooth.cs.sevent.step.ctExtension.get(channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: cs_tone_ext: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CTEXtension?')
		return Conversions.str_to_bool(response)
