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

	def set(self, ipart_instr_name: List[str], rf_path: str = None, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:ISELect \n
		Snippet: driver.sconfiguration.external.iqOutput.remote.iselect.set(ipart_instr_name = ['abc1', 'abc2', 'abc3'], rf_path = 'abc', iqConnector = repcap.IqConnector.Default) \n
		Select an external instrument for the selected connector. \n
			:param ipart_instr_name: String Instrument alias name, as retrieved with the command method RsSmbv.Sconfiguration.External.Remote.listPy or defined with the command method RsSmbv.Sconfiguration.External.Remote.Add.set.
			:param rf_path: String Determines the used RF output of the external instrument.
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('ipart_instr_name', ipart_instr_name, DataType.StringList, None), ArgSingle('rf_path', rf_path, DataType.String, None, is_optional=True))
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:ISELect {param}'.rstrip())

	# noinspection PyTypeChecker
	class IselectStruct(StructBase):
		"""Response structure. Fields: \n
			- Ipart_Instr_Name: List[str]: No parameter help available
			- Rf_Path: str: String Determines the used RF output of the external instrument."""
		__meta_args_list = [
			ArgStruct('Ipart_Instr_Name', DataType.StringList, None, False, True, 1),
			ArgStruct.scalar_str('Rf_Path')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ipart_Instr_Name: List[str] = None
			self.Rf_Path: str = None

	def get(self, iqConnector=repcap.IqConnector.Default) -> IselectStruct:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:ISELect \n
		Snippet: value: IselectStruct = driver.sconfiguration.external.iqOutput.remote.iselect.get(iqConnector = repcap.IqConnector.Default) \n
		Select an external instrument for the selected connector. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: structure: for return value, see the help for IselectStruct structure arguments."""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		return self._core.io.query_struct(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:ISELect?', self.__class__.IselectStruct())
