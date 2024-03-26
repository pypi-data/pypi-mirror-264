from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoteCls:
	"""Remote commands group definition. 10 total commands, 7 Subgroups, 1 group commands"""

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
	def detect(self):
		"""detect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_detect'):
			from .Detect import DetectCls
			self._detect = DetectCls(self._core, self._cmd_group)
		return self._detect

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

	def send(self, send_scpi_command: str, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:REMote:SEND \n
		Snippet: driver.sconfiguration.external.digital.remote.send(send_scpi_command = 'abc', index = repcap.Index.Default) \n
		No command help available \n
			:param send_scpi_command: No help available
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
		"""
		param = Conversions.value_to_quoted_str(send_scpi_command)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:REMote:SEND {param}')

	def clone(self) -> 'RemoteCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RemoteCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
