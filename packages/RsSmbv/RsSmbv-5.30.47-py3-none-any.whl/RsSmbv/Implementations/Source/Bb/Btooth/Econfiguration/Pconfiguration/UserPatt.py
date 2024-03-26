from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserPattCls:
	"""UserPatt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("userPatt", core, parent)

	def set(self, user_patt: List[str], bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.userPatt.set(user_patt = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1) \n
		No command help available \n
			:param user_patt: No help available
			:param bitcount: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('user_patt', user_patt, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt {param}'.rstrip())

	# noinspection PyTypeChecker
	class UserPattStruct(StructBase):
		"""Response structure. Fields: \n
			- User_Patt: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('User_Patt', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.User_Patt: List[str] = None
			self.Bitcount: int = None

	def get(self) -> UserPattStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt \n
		Snippet: value: UserPattStruct = driver.source.bb.btooth.econfiguration.pconfiguration.userPatt.get() \n
		No command help available \n
			:return: structure: for return value, see the help for UserPattStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:USERpatt?', self.__class__.UserPattStruct())
