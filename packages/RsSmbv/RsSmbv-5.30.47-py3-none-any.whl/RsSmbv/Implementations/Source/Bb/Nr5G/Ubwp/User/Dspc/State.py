from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, data_source_uniq: bool, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:DSPC:STATe \n
		Snippet: driver.source.bb.nr5G.ubwp.user.dspc.state.set(data_source_uniq = False, userNull = repcap.UserNull.Default) \n
		Turns usage of a unique data source for the PDSCH in a multi-carrier scenario on and off. \n
			:param data_source_uniq: 1| ON| 0| OFF
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(data_source_uniq)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:DSPC:STATe {param}')

	def get(self, userNull=repcap.UserNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:DSPC:STATe \n
		Snippet: value: bool = driver.source.bb.nr5G.ubwp.user.dspc.state.get(userNull = repcap.UserNull.Default) \n
		Turns usage of a unique data source for the PDSCH in a multi-carrier scenario on and off. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: data_source_uniq: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:DSPC:STATe?')
		return Conversions.str_to_bool(response)
