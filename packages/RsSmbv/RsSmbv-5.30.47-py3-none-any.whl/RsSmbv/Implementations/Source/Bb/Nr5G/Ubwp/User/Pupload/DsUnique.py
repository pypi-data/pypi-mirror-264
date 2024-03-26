from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DsUniqueCls:
	"""DsUnique commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dsUnique", core, parent)

	def set(self, ds_unique: bool, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUPLoad:DSUNique \n
		Snippet: driver.source.bb.nr5G.ubwp.user.pupload.dsUnique.set(ds_unique = False, userNull = repcap.UserNull.Default) \n
		Turns selection of different data sources for the PUCCH payload on and off. If off, you can select a data source with
		[:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUPLoad:DATA. \n
			:param ds_unique: 1| ON| 0| OFF
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(ds_unique)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUPLoad:DSUNique {param}')

	def get(self, userNull=repcap.UserNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUPLoad:DSUNique \n
		Snippet: value: bool = driver.source.bb.nr5G.ubwp.user.pupload.dsUnique.get(userNull = repcap.UserNull.Default) \n
		Turns selection of different data sources for the PUCCH payload on and off. If off, you can select a data source with
		[:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUPLoad:DATA. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: ds_unique: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUPLoad:DSUNique?')
		return Conversions.str_to_bool(response)
