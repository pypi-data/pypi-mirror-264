from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoteCls:
	"""Remote commands group definition. 9 total commands, 6 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("remote", core, parent)

	@property
	def connect(self):
		"""connect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connect'):
			from .Connect import ConnectCls
			self._connect = ConnectCls(self._core, self._cmd_group)
		return self._connect

	@property
	def disconnect(self):
		"""disconnect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_disconnect'):
			from .Disconnect import DisconnectCls
			self._disconnect = DisconnectCls(self._core, self._cmd_group)
		return self._disconnect

	@property
	def iconnect(self):
		"""iconnect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iconnect'):
			from .Iconnect import IconnectCls
			self._iconnect = IconnectCls(self._core, self._cmd_group)
		return self._iconnect

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def initialization(self):
		"""initialization commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_initialization'):
			from .Initialization import InitializationCls
			self._initialization = InitializationCls(self._core, self._cmd_group)
		return self._initialization

	@property
	def iselect(self):
		"""iselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iselect'):
			from .Iselect import IselectCls
			self._iselect = IselectCls(self._core, self._cmd_group)
		return self._iselect

	def send(self, send_scpi_command: str, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:REMote:SEND \n
		Snippet: driver.sconfiguration.external.bbmm.remote.send(send_scpi_command = 'abc', iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param send_scpi_command: No help available
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = Conversions.value_to_quoted_str(send_scpi_command)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:REMote:SEND {param}')

	def clone(self) -> 'RemoteCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RemoteCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
