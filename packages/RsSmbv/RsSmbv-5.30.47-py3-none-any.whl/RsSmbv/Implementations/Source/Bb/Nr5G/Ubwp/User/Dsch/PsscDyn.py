from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PsscDynCls:
	"""PsscDyn commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("psscDyn", core, parent)

	def set(self, ss_cell_dyn: bool, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:DSCH:PSSCdyn \n
		Snippet: driver.source.bb.nr5G.ubwp.user.dsch.psscDyn.set(ss_cell_dyn = False, userNull = repcap.UserNull.Default) \n
		Turns the 'PUCCH Cell Indicator' field available in DCI format 1_1 on and off. \n
			:param ss_cell_dyn: 1| ON| 0| OFF
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.bool_to_str(ss_cell_dyn)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:DSCH:PSSCdyn {param}')

	def get(self, userNull=repcap.UserNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:DSCH:PSSCdyn \n
		Snippet: value: bool = driver.source.bb.nr5G.ubwp.user.dsch.psscDyn.get(userNull = repcap.UserNull.Default) \n
		Turns the 'PUCCH Cell Indicator' field available in DCI format 1_1 on and off. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: ss_cell_dyn: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:DSCH:PSSCdyn?')
		return Conversions.str_to_bool(response)
