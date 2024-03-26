from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EcodeCls:
	"""Ecode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ecode", core, parent)

	def set(self, ecode: List[str], bitcount: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ECODe \n
		Snippet: driver.source.bb.btooth.cs.cdata.ecode.set(ecode = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1) \n
		No command help available \n
			:param ecode: No help available
			:param bitcount: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('ecode', ecode, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ECODe {param}'.rstrip())

	# noinspection PyTypeChecker
	class EcodeStruct(StructBase):
		"""Response structure. Fields: \n
			- Ecode: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Ecode', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ecode: List[str] = None
			self.Bitcount: int = None

	def get(self) -> EcodeStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CDATa:ECODe \n
		Snippet: value: EcodeStruct = driver.source.bb.btooth.cs.cdata.ecode.get() \n
		No command help available \n
			:return: structure: for return value, see the help for EcodeStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:CDATa:ECODe?', self.__class__.EcodeStruct())
