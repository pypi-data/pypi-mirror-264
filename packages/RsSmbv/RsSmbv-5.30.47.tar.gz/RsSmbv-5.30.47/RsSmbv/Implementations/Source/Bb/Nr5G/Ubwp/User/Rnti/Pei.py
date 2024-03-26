from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PeiCls:
	"""Pei commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pei", core, parent)

	def set(self, peir_nti: int, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:RNTI:PEI \n
		Snippet: driver.source.bb.nr5G.ubwp.user.rnti.pei.set(peir_nti = 1, userNull = repcap.UserNull.Default) \n
		Sets the PEI-RNTI of the user. \n
			:param peir_nti: integer For release 17, the MCCH-RNTI has a fix value of 65532. Range: 1 to 65532
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.decimal_value_to_str(peir_nti)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:RNTI:PEI {param}')

	def get(self, userNull=repcap.UserNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:RNTI:PEI \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.rnti.pei.get(userNull = repcap.UserNull.Default) \n
		Sets the PEI-RNTI of the user. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: peir_nti: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:RNTI:PEI?')
		return Conversions.str_to_int(response)
