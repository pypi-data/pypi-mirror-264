from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	def set(self, pattern: List[str], bitcount: int, userNull=repcap.UserNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:SSCH:PATTern \n
		Snippet: driver.source.bb.nr5G.ubwp.user.ssch.pattern.set(pattern = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1, userNull = repcap.UserNull.Default) \n
		Defines a bit pattern as the PSSCH data source.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select bit pattern as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:SSCH:DATA) . \n
			:param pattern: 64 bits
			:param bitcount: integer Range: 1 to 64
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('pattern', pattern, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:SSCH:PATTern {param}'.rstrip())

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Response structure. Fields: \n
			- Pattern: List[str]: 64 bits
			- Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def get(self, userNull=repcap.UserNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:SSCH:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nr5G.ubwp.user.ssch.pattern.get(userNull = repcap.UserNull.Default) \n
		Defines a bit pattern as the PSSCH data source.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select bit pattern as data source ([:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:SSCH:DATA) . \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:SSCH:PATTern?', self.__class__.PatternStruct())
