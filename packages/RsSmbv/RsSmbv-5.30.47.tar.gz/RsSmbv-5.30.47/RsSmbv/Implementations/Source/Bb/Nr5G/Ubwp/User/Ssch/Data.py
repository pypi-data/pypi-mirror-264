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

	def set(self, ssch_data_source: enums.DataSourceA, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:SSCH:DATA \n
		Snippet: driver.source.bb.nr5G.ubwp.user.ssch.data.set(ssch_data_source = enums.DataSourceA.DLISt, userNull = repcap.UserNull.Default) \n
		Selects the data source for the PSSCH. \n
			:param ssch_data_source: DLISt Data source is binary data from a data list. Select the data list with [:SOURcehw]:BB:NR5G:UBWP:USERus:SSCH:DLISt. PATTern Data source is a equence according to a bit pattern. Define the bit pattern with [:SOURcehw]:BB:NR5G:UBWP:USERus:SSCH:PATTern. PN9 | PN11 | PN15 | PN16 | PN20 | PN21 | PN23 Data source is a pseudo-random sequence. Set the initial value with [:SOURcehw]:BB:NR5G:UBWP:USERus:SSCH:INITpattern. ZERO | ONE Data source is a sequence containing all 0's or all 1's.
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(ssch_data_source, enums.DataSourceA)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:SSCH:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, userNull=repcap.UserNull.Default) -> enums.DataSourceA:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:SSCH:DATA \n
		Snippet: value: enums.DataSourceA = driver.source.bb.nr5G.ubwp.user.ssch.data.get(userNull = repcap.UserNull.Default) \n
		Selects the data source for the PSSCH. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: ssch_data_source: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:SSCH:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceA)
