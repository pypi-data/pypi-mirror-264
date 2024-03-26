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

	def set(self, ipart_instr_name: List[str], rf_path: str, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:ICONnect \n
		Snippet: driver.sconfiguration.external.iqOutput.remote.iconnect.set(ipart_instr_name = ['abc1', 'abc2', 'abc3'], rf_path = 'abc', iqConnector = repcap.IqConnector.Default) \n
		Selects an external instrument for the selected connector and triggers connection. \n
			:param ipart_instr_name: string Instrument alias name, as retrieved with the command method RsSmbv.Sconfiguration.External.Remote.listPy or defined with the command method RsSmbv.Sconfiguration.External.Remote.Add.set.
			:param rf_path: string Determines the used RF output of the external instrument. For a one-path instrument, the output path is fixed.
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('ipart_instr_name', ipart_instr_name, DataType.StringList, None), ArgSingle('rf_path', rf_path, DataType.String))
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:ICONnect {param}'.rstrip())
