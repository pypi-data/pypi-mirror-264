from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CinpCls:
	"""Cinp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cinp", core, parent)

	def set(self, cs_in_p: List[str], bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINP \n
		Snippet: driver.source.bb.btooth.cs.cinp.set(cs_in_p = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1) \n
		No command help available \n
			:param cs_in_p: No help available
			:param bitcount: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('cs_in_p', cs_in_p, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CINP {param}'.rstrip())

	# noinspection PyTypeChecker
	class CinpStruct(StructBase):
		"""Response structure. Fields: \n
			- Cs_In_P: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Cs_In_P', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_In_P: List[str] = None
			self.Bitcount: int = None

	def get(self) -> CinpStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINP \n
		Snippet: value: CinpStruct = driver.source.bb.btooth.cs.cinp.get() \n
		No command help available \n
			:return: structure: for return value, see the help for CinpStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CINP?', self.__class__.CinpStruct())
