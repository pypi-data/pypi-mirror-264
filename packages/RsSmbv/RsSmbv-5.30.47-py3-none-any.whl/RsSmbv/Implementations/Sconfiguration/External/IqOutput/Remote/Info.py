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

	def get(self, iqConnector=repcap.IqConnector.Default) -> List[str]:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:INFO \n
		Snippet: value: List[str] = driver.sconfiguration.external.iqOutput.remote.info.get(iqConnector = repcap.IqConnector.Default) \n
		Queries information on the external instrument. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: ipartd_pi_db_ext_dev_rem_inst_info: string Returns information in one of the following formats: 'None' An external instrument is not assigned SymbolicName,RemoteChannel,RemoteAddress,RF Path An external instrument is assigned, but not connected SymbolicName,RemoteChannel,RemoteAddress,RF Path[,*IDN? String] An external instrument is assigned and connected"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:INFO?')
		return Conversions.str_to_str_list(response)
