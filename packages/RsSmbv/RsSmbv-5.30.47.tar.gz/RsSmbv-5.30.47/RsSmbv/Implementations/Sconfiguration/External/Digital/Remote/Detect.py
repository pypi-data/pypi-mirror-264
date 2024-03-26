from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DetectCls:
	"""Detect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("detect", core, parent)

	def get(self, index=repcap.Index.Default) -> str:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:REMote:DETect \n
		Snippet: value: str = driver.sconfiguration.external.digital.remote.detect.get(index = repcap.Index.Default) \n
		Searches for external instruments connected to the particular digital interfaces. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:return: detected_instr: string If the detection fails, the query returns 'None'."""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:REMote:DETect?')
		return trim_str_response(response)
