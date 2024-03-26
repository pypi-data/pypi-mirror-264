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

	def set(self, instr_name: List[str], rf_path: str, digitalIq=repcap.DigitalIq.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:REMote:ICONnect \n
		Snippet: driver.sconfiguration.external.fader.remote.iconnect.set(instr_name = ['abc1', 'abc2', 'abc3'], rf_path = 'abc', digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param instr_name: No help available
			:param rf_path: No help available
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('instr_name', instr_name, DataType.StringList, None), ArgSingle('rf_path', rf_path, DataType.String))
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		self._core.io.write(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:REMote:ICONnect {param}'.rstrip())
