from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SetCls:
	"""Set commands group definition. 4 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("set", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, channel: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._cmd_group.set_repcap_enum_value(channel)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cfOffset(self):
		"""cfOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfOffset'):
			from .CfOffset import CfOffsetCls
			self._cfOffset = CfOffsetCls(self._core, self._cmd_group)
		return self._cfOffset

	@property
	def mindex(self):
		"""mindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mindex'):
			from .Mindex import MindexCls
			self._mindex = MindexCls(self._core, self._cmd_group)
		return self._mindex

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def stError(self):
		"""stError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stError'):
			from .StError import StErrorCls
			self._stError = StErrorCls(self._core, self._cmd_group)
		return self._stError

	def clone(self) -> 'SetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
