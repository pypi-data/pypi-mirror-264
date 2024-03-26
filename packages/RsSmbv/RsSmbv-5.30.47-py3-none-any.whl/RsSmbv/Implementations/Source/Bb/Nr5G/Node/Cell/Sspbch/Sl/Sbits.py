from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SbitsCls:
	"""Sbits commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sbits", core, parent)

	def set(self, pattern: List[str], bitcount: int, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:SL:SBITs \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.sl.sbits.set(pattern = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines the spare bits for the PSBCH. \n
			:param pattern: 2 bits
			:param bitcount: integer Range: 2 to 2
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('pattern', pattern, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:SL:SBITs {param}'.rstrip())

	# noinspection PyTypeChecker
	class SbitsStruct(StructBase):
		"""Response structure. Fields: \n
			- Pattern: List[str]: 2 bits
			- Bitcount: int: integer Range: 2 to 2"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> SbitsStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:SL:SBITs \n
		Snippet: value: SbitsStruct = driver.source.bb.nr5G.node.cell.sspbch.sl.sbits.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines the spare bits for the PSBCH. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: structure: for return value, see the help for SbitsStruct structure arguments."""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:SL:SBITs?', self.__class__.SbitsStruct())
