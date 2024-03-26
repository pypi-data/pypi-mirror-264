from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsdsCls:
	"""Usds commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("usds", core, parent)

	def set(self, use_oran_ds: bool, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:ORAN:USDS \n
		Snippet: driver.source.bb.nr5G.ubwp.user.oran.usds.set(use_oran_ds = False, userNull = repcap.UserNull.Default) \n
		Turns usage of the PxSCH data source according to the ORAN standard on and off. \n
			:param use_oran_ds: 1| ON| 0| OFF
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(use_oran_ds)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:ORAN:USDS {param}')

	def get(self, userNull=repcap.UserNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:ORAN:USDS \n
		Snippet: value: bool = driver.source.bb.nr5G.ubwp.user.oran.usds.get(userNull = repcap.UserNull.Default) \n
		Turns usage of the PxSCH data source according to the ORAN standard on and off. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: use_oran_ds: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:ORAN:USDS?')
		return Conversions.str_to_bool(response)
