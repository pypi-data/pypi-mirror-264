from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DisconnectCls:
	"""Disconnect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("disconnect", core, parent)

	def set(self, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:REMote:DISConnect \n
		Snippet: driver.sconfiguration.external.digital.remote.disconnect.set(index = repcap.Index.Default) \n
		Disconnects the selected remote connection. To disconnect all remote connections at once, use the command method RsSmbv.
		Sconfiguration.External.Remote.Disconnect.All.set. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
		"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:REMote:DISConnect')

	def set_with_opc(self, index=repcap.Index.Default, opc_timeout_ms: int = -1) -> None:
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:REMote:DISConnect \n
		Snippet: driver.sconfiguration.external.digital.remote.disconnect.set_with_opc(index = repcap.Index.Default) \n
		Disconnects the selected remote connection. To disconnect all remote connections at once, use the command method RsSmbv.
		Sconfiguration.External.Remote.Disconnect.All.set. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:REMote:DISConnect', opc_timeout_ms)
