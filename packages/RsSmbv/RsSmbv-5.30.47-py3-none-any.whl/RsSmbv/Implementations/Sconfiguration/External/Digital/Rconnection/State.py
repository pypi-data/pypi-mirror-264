from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def get(self, index=repcap.Index.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:RCONnection:STATe \n
		Snippet: value: bool = driver.sconfiguration.external.digital.rconnection.state.get(index = repcap.Index.Default) \n
		Queries the status of the remote connection. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:return: state: 1| ON| 0| OFF"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:RCONnection:STATe?')
		return Conversions.str_to_bool(response)
