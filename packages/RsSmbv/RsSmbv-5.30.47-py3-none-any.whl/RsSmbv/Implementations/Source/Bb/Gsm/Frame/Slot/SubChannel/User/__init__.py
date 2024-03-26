from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 27 total commands, 13 Subgroups, 0 group commands
	Repeated Capability: UserIx, default value after init: UserIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_userIx_get', 'repcap_userIx_set', repcap.UserIx.Nr1)

	def repcap_userIx_set(self, userIx: repcap.UserIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserIx.Default
		Default value after init: UserIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(userIx)

	def repcap_userIx_get(self) -> repcap.UserIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def attenuation(self):
		"""attenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_attenuation'):
			from .Attenuation import AttenuationCls
			self._attenuation = AttenuationCls(self._core, self._cmd_group)
		return self._attenuation

	@property
	def dummy(self):
		"""dummy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dummy'):
			from .Dummy import DummyCls
			self._dummy = DummyCls(self._core, self._cmd_group)
		return self._dummy

	@property
	def etsc(self):
		"""etsc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_etsc'):
			from .Etsc import EtscCls
			self._etsc = EtscCls(self._core, self._cmd_group)
		return self._etsc

	@property
	def fcorrection(self):
		"""fcorrection commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcorrection'):
			from .Fcorrection import FcorrectionCls
			self._fcorrection = FcorrectionCls(self._core, self._cmd_group)
		return self._fcorrection

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	@property
	def predefined(self):
		"""predefined commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	@property
	def scpiRatio(self):
		"""scpiRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scpiRatio'):
			from .ScpiRatio import ScpiRatioCls
			self._scpiRatio = ScpiRatioCls(self._core, self._cmd_group)
		return self._scpiRatio

	@property
	def sflag(self):
		"""sflag commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sflag'):
			from .Sflag import SflagCls
			self._sflag = SflagCls(self._core, self._cmd_group)
		return self._sflag

	@property
	def sync(self):
		"""sync commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Sync import SyncCls
			self._sync = SyncCls(self._core, self._cmd_group)
		return self._sync

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def ulist(self):
		"""ulist commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_ulist'):
			from .Ulist import UlistCls
			self._ulist = UlistCls(self._core, self._cmd_group)
		return self._ulist

	@property
	def source(self):
		"""source commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_source'):
			from .Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	def clone(self) -> 'UserCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UserCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
