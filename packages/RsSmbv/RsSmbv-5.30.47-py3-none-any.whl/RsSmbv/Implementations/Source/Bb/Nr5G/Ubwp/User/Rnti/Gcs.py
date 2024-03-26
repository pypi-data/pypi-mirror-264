from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GcsCls:
	"""Gcs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gcs", core, parent)

	def set(self, gc_srnti: int, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:RNTI:GCS \n
		Snippet: driver.source.bb.nr5G.ubwp.user.rnti.gcs.set(gc_srnti = 1, userNull = repcap.UserNull.Default) \n
		Sets the G-CS-RNTI of the user. \n
			:param gc_srnti: integer Range: 1 to 65519
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.decimal_value_to_str(gc_srnti)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:RNTI:GCS {param}')

	def get(self, userNull=repcap.UserNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:RNTI:GCS \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.rnti.gcs.get(userNull = repcap.UserNull.Default) \n
		Sets the G-CS-RNTI of the user. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: gc_srnti: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:RNTI:GCS?')
		return Conversions.str_to_int(response)
