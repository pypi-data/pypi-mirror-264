from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfCls:
	"""Rf commands group definition. 18 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: Path, default value after init: Path.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rf", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_path_get', 'repcap_path_set', repcap.Path.Nr1)

	def repcap_path_set(self, path: repcap.Path) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Path.Default
		Default value after init: Path.Nr1"""
		self._cmd_group.set_repcap_enum_value(path)

	def repcap_path_get(self) -> repcap.Path:
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
	def rconnection(self):
		"""rconnection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rconnection'):
			from .Rconnection import RconnectionCls
			self._rconnection = RconnectionCls(self._core, self._cmd_group)
		return self._rconnection

	@property
	def remote(self):
		"""remote commands group. 6 Sub-classes, 1 commands."""
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

	def clone(self) -> 'RfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
