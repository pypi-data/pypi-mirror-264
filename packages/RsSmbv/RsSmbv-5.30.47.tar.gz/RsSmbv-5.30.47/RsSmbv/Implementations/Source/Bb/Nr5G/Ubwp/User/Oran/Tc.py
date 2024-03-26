from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TcCls:
	"""Tc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tc", core, parent)

	def set(self, oran_tc: enums.OranTcAll, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:ORAN:TC \n
		Snippet: driver.source.bb.nr5G.ubwp.user.oran.tc.set(oran_tc = enums.OranTcAll.TC3231_1, userNull = repcap.UserNull.Default) \n
		Selects the ORAN test case for ORAN data generation.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on ORAN compliant data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:ORAN:USDS) . \n
			:param oran_tc: TC3231_1| TC3231_2| TC3231_3| TC3231_4| TC3231_5| TC3231_6| TC3231_7| TC3231_8| TC3231_9| TC3231_10| TC3231_11| TC3231_12| TC3231_13| TC3231_14| TC3231_15| TC3231_16| TC3231_17| TC3251_1| TC3251_2| TC3251_3DL| TC3251_3UL| TC3251_5| TC3251_7| TC3251_8DL| TC3251_8UL| TC3251_4DL| TC3251_4UL| TC3261_1DL| TC3261_1UL| TC3261_3DL| TC3261_3UL| TC3261_5DL| TC3261_5UL| TC3261_6DL| TC3261_6UL
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(oran_tc, enums.OranTcAll)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:ORAN:TC {param}')

	# noinspection PyTypeChecker
	def get(self, userNull=repcap.UserNull.Default) -> enums.OranTcAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:ORAN:TC \n
		Snippet: value: enums.OranTcAll = driver.source.bb.nr5G.ubwp.user.oran.tc.get(userNull = repcap.UserNull.Default) \n
		Selects the ORAN test case for ORAN data generation.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on ORAN compliant data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:ORAN:USDS) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: oran_tc: TC3231_1| TC3231_2| TC3231_3| TC3231_4| TC3231_5| TC3231_6| TC3231_7| TC3231_8| TC3231_9| TC3231_10| TC3231_11| TC3231_12| TC3231_13| TC3231_14| TC3231_15| TC3231_16| TC3231_17| TC3251_1| TC3251_2| TC3251_3DL| TC3251_3UL| TC3251_5| TC3251_7| TC3251_8DL| TC3251_8UL| TC3251_4DL| TC3251_4UL| TC3261_1DL| TC3261_1UL| TC3261_3DL| TC3261_3UL| TC3261_5DL| TC3261_5UL| TC3261_6DL| TC3261_6UL"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:ORAN:TC?')
		return Conversions.str_to_scalar_enum(response, enums.OranTcAll)
