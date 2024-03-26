from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NsasCls:
	"""Nsas commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nsas", core, parent)

	def set(self, slai_size: int, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:USCH:NSAS \n
		Snippet: driver.source.bb.nr5G.ubwp.user.usch.nsas.set(slai_size = 1, userNull = repcap.UserNull.Default) \n
		Defines the size of the 'Sidelink Assignment Index' in DCI format 3_0. \n
			:param slai_size: integer Range: 0 to 2
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.decimal_value_to_str(slai_size)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:USCH:NSAS {param}')

	def get(self, userNull=repcap.UserNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:USCH:NSAS \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.usch.nsas.get(userNull = repcap.UserNull.Default) \n
		Defines the size of the 'Sidelink Assignment Index' in DCI format 3_0. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: slai_size: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:USCH:NSAS?')
		return Conversions.str_to_int(response)
