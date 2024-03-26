from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DisconnectCls:
	"""Disconnect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("disconnect", core, parent)

	def set(self, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:DISConnect \n
		Snippet: driver.sconfiguration.external.iqOutput.remote.disconnect.set(iqConnector = repcap.IqConnector.Default) \n
		Disconnects the selected remote connection. To disconnect all remote connections at once, use the command method RsSmbv.
		Sconfiguration.External.Remote.Disconnect.All.set. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:DISConnect')

	def set_with_opc(self, iqConnector=repcap.IqConnector.Default, opc_timeout_ms: int = -1) -> None:
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:REMote:DISConnect \n
		Snippet: driver.sconfiguration.external.iqOutput.remote.disconnect.set_with_opc(iqConnector = repcap.IqConnector.Default) \n
		Disconnects the selected remote connection. To disconnect all remote connections at once, use the command method RsSmbv.
		Sconfiguration.External.Remote.Disconnect.All.set. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:REMote:DISConnect', opc_timeout_ms)
