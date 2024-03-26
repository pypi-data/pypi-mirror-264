from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	def set(self, data_source: enums.DataSourceA, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUPLoad:DATA \n
		Snippet: driver.source.bb.nr5G.ubwp.user.pupload.data.set(data_source = enums.DataSourceA.DLISt, userNull = repcap.UserNull.Default) \n
		Selects the data source for the PUSCH UCI.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Allow selection of data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUPLoad:DSUNique) . \n
			:param data_source: ONE | ZERO Data source is a sequence that contains only '0' or '1'. DLISt Data source is a sequence based on a binary data list. PATTern Data source is sequence based on a bit pattern. PN9 | PN11 | PN15 | PN16 | PN20 | PN21 | PN23 Data source is a pseudo-random sequence.
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(data_source, enums.DataSourceA)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUPLoad:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, userNull=repcap.UserNull.Default) -> enums.DataSourceA:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUPLoad:DATA \n
		Snippet: value: enums.DataSourceA = driver.source.bb.nr5G.ubwp.user.pupload.data.get(userNull = repcap.UserNull.Default) \n
		Selects the data source for the PUSCH UCI.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Allow selection of data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUPLoad:DSUNique) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: data_source: ONE | ZERO Data source is a sequence that contains only '0' or '1'. DLISt Data source is a sequence based on a binary data list. PATTern Data source is sequence based on a bit pattern. PN9 | PN11 | PN15 | PN16 | PN20 | PN21 | PN23 Data source is a pseudo-random sequence."""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUPLoad:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceA)
