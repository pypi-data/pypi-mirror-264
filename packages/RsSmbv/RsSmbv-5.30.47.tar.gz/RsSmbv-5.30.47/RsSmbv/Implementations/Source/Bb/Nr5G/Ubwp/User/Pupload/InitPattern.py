from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InitPatternCls:
	"""InitPattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("initPattern", core, parent)

	def set(self, pattern_init: int, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUPLoad:INITpattern \n
		Snippet: driver.source.bb.nr5G.ubwp.user.pupload.initPattern.set(pattern_init = 1, userNull = repcap.UserNull.Default) \n
		Sets an initialization value for the second m-sequence in the PN sequence.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a PN sequence as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUPLoad:DATA) . \n
			:param pattern_init: integer Range: 1 to 0x7fffff
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = Conversions.decimal_value_to_str(pattern_init)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUPLoad:INITpattern {param}')

	def get(self, userNull=repcap.UserNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:PUPLoad:INITpattern \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.pupload.initPattern.get(userNull = repcap.UserNull.Default) \n
		Sets an initialization value for the second m-sequence in the PN sequence.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a PN sequence as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:PUPLoad:DATA) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: pattern_init: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:PUPLoad:INITpattern?')
		return Conversions.str_to_int(response)
