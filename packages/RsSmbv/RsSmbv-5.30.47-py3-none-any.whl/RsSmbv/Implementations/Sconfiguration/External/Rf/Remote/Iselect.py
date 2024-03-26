from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IselectCls:
	"""Iselect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iselect", core, parent)

	def set(self, instr_name: List[str], rf_path: str = None, path=repcap.Path.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:REMote:ISELect \n
		Snippet: driver.sconfiguration.external.rf.remote.iselect.set(instr_name = ['abc1', 'abc2', 'abc3'], rf_path = 'abc', path = repcap.Path.Default) \n
		No command help available \n
			:param instr_name: No help available
			:param rf_path: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('instr_name', instr_name, DataType.StringList, None), ArgSingle('rf_path', rf_path, DataType.String, None, is_optional=True))
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SCONfiguration:EXTernal:RF{path_cmd_val}:REMote:ISELect {param}'.rstrip())

	# noinspection PyTypeChecker
	class IselectStruct(StructBase):
		"""Response structure. Fields: \n
			- Instr_Name: List[str]: No parameter help available
			- Rf_Path: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Instr_Name', DataType.StringList, None, False, True, 1),
			ArgStruct.scalar_str('Rf_Path')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Instr_Name: List[str] = None
			self.Rf_Path: str = None

	def get(self, path=repcap.Path.Default) -> IselectStruct:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:REMote:ISELect \n
		Snippet: value: IselectStruct = driver.sconfiguration.external.rf.remote.iselect.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: structure: for return value, see the help for IselectStruct structure arguments."""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		return self._core.io.query_struct(f'SCONfiguration:EXTernal:RF{path_cmd_val}:REMote:ISELect?', self.__class__.IselectStruct())
