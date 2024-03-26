from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IconnectCls:
	"""Iconnect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iconnect", core, parent)

	def set(self, instr_name: List[str], rf_path: str, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:REMote:ICONnect \n
		Snippet: driver.sconfiguration.external.hsDigital.remote.iconnect.set(instr_name = ['abc1', 'abc2', 'abc3'], rf_path = 'abc', index = repcap.Index.Default) \n
		Selects an external instrument for the selected connector and triggers connection. \n
			:param instr_name: string Instrument alias name, as retrieved with the command method RsSmbv.Sconfiguration.External.Remote.listPy or defined with the command method RsSmbv.Sconfiguration.External.Remote.Add.set.
			:param rf_path: string Determines the used RF output of the external instrument. For a one-path instrument, the output path is fixed.
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('instr_name', instr_name, DataType.StringList, None), ArgSingle('rf_path', rf_path, DataType.String))
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:REMote:ICONnect {param}'.rstrip())
