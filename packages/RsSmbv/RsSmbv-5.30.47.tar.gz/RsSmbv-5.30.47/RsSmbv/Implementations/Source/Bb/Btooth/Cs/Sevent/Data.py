from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	def set(self, data_source: enums.DataSourceB, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:DATA \n
		Snippet: driver.source.bb.btooth.cs.sevent.data.set(data_source = enums.DataSourceB.ALL0, channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param data_source: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(data_source, enums.DataSourceB)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.DataSourceB:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:DATA \n
		Snippet: value: enums.DataSourceB = driver.source.bb.btooth.cs.sevent.data.get(channelNull = repcap.ChannelNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: data_source: No help available"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceB)
