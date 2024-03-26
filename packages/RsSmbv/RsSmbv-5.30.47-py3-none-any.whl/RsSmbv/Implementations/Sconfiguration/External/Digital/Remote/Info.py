from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InfoCls:
	"""Info commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("info", core, parent)

	def get(self, index=repcap.Index.Default) -> List[str]:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:REMote:INFO \n
		Snippet: value: List[str] = driver.sconfiguration.external.digital.remote.info.get(index = repcap.Index.Default) \n
		Queries information on the external instrument. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:return: id_pi_db_ext_dev_rem_inst_info: string Returns information in one of the following formats: 'None' An external instrument is not assigned SymbolicName,RemoteChannel,RemoteAddress,RF Path An external instrument is assigned, but not connected SymbolicName,RemoteChannel,RemoteAddress,RF Path[,*IDN? String] An external instrument is assigned and connected"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:REMote:INFO?')
		return Conversions.str_to_str_list(response)
