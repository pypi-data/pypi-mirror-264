from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UpPatternCls:
	"""UpPattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("upPattern", core, parent)

	def set(self, pattern: enums.BtoCsPyLdPatt, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:UPPattern \n
		Snippet: driver.source.bb.btooth.cs.sevent.upPattern.set(pattern = enums.BtoCsPyLdPatt.PRBS09, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param pattern: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.BtoCsPyLdPatt)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:UPPattern {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsPyLdPatt:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:UPPattern \n
		Snippet: value: enums.BtoCsPyLdPatt = driver.source.bb.btooth.cs.sevent.upPattern.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: pattern: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:UPPattern?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsPyLdPatt)
