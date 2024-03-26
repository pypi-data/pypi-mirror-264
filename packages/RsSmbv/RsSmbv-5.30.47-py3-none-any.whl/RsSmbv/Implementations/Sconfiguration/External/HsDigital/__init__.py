from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HsDigitalCls:
	"""HsDigital commands group definition. 20 total commands, 6 Subgroups, 0 group commands
	Repeated Capability: Index, default value after init: Index.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hsDigital", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_index_get', 'repcap_index_set', repcap.Index.Nr1)

	def repcap_index_set(self, index: repcap.Index) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Index.Default
		Default value after init: Index.Nr1"""
		self._cmd_group.set_repcap_enum_value(index)

	def repcap_index_get(self) -> repcap.Index:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def direction(self):
		"""direction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direction'):
			from .Direction import DirectionCls
			self._direction = DirectionCls(self._core, self._cmd_group)
		return self._direction

	@property
	def iname(self):
		"""iname commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iname'):
			from .Iname import InameCls
			self._iname = InameCls(self._core, self._cmd_group)
		return self._iname

	@property
	def iqConnection(self):
		"""iqConnection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqConnection'):
			from .IqConnection import IqConnectionCls
			self._iqConnection = IqConnectionCls(self._core, self._cmd_group)
		return self._iqConnection

	@property
	def rconnection(self):
		"""rconnection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rconnection'):
			from .Rconnection import RconnectionCls
			self._rconnection = RconnectionCls(self._core, self._cmd_group)
		return self._rconnection

	@property
	def remote(self):
		"""remote commands group. 7 Sub-classes, 1 commands."""
		if not hasattr(self, '_remote'):
			from .Remote import RemoteCls
			self._remote = RemoteCls(self._core, self._cmd_group)
		return self._remote

	@property
	def rf(self):
		"""rf commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import RfCls
			self._rf = RfCls(self._core, self._cmd_group)
		return self._rf

	def clone(self) -> 'HsDigitalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HsDigitalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
