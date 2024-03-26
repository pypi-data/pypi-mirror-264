from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CincCls:
	"""Cinc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cinc", core, parent)

	def set(self, cs_in_c: List[str], bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINC \n
		Snippet: driver.source.bb.btooth.cs.cinc.set(cs_in_c = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1) \n
		No command help available \n
			:param cs_in_c: No help available
			:param bitcount: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('cs_in_c', cs_in_c, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CINC {param}'.rstrip())

	# noinspection PyTypeChecker
	class CincStruct(StructBase):
		"""Response structure. Fields: \n
			- Cs_In_C: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Cs_In_C', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_In_C: List[str] = None
			self.Bitcount: int = None

	def get(self) -> CincStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINC \n
		Snippet: value: CincStruct = driver.source.bb.btooth.cs.cinc.get() \n
		No command help available \n
			:return: structure: for return value, see the help for CincStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CINC?', self.__class__.CincStruct())
