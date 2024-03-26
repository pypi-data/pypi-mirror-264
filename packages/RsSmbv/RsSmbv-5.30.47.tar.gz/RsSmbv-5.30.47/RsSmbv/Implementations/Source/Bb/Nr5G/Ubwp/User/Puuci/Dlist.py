from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DlistCls:
	"""Dlist commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dlist", core, parent)

	def set(self, data_list: str, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUUCi:DLISt \n
		Snippet: driver.source.bb.nr5G.ubwp.user.puuci.dlist.set(data_list = 'abc', userNull = repcap.UserNull.Default) \n
		Selects an existing data list file from the default directory or from the specific directory.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a file as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUUCi:DATA) . \n
			:param data_list: string
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.value_to_quoted_str(data_list)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUUCi:DLISt {param}')

	def get(self, userNull=repcap.UserNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUUCi:DLISt \n
		Snippet: value: str = driver.source.bb.nr5G.ubwp.user.puuci.dlist.get(userNull = repcap.UserNull.Default) \n
		Selects an existing data list file from the default directory or from the specific directory.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a file as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUUCi:DATA) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: data_list: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUUCi:DLISt?')
		return trim_str_response(response)
