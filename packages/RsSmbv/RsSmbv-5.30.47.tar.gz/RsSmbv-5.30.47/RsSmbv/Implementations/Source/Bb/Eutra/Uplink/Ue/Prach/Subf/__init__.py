from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubfCls:
	"""Subf commands group definition. 8 total commands, 8 Subgroups, 0 group commands
	Repeated Capability: SubframeNull, default value after init: SubframeNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subf", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_subframeNull_get', 'repcap_subframeNull_set', repcap.SubframeNull.Nr0)

	def repcap_subframeNull_set(self, subframeNull: repcap.SubframeNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubframeNull.Default
		Default value after init: SubframeNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(subframeNull)

	def repcap_subframeNull_get(self) -> repcap.SubframeNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def dt(self):
		"""dt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dt'):
			from .Dt import DtCls
			self._dt = DtCls(self._core, self._cmd_group)
		return self._dt

	@property
	def frIndex(self):
		"""frIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frIndex'):
			from .FrIndex import FrIndexCls
			self._frIndex = FrIndexCls(self._core, self._cmd_group)
		return self._frIndex

	@property
	def ncsConf(self):
		"""ncsConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncsConf'):
			from .NcsConf import NcsConfCls
			self._ncsConf = NcsConfCls(self._core, self._cmd_group)
		return self._ncsConf

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .RbOffset import RbOffsetCls
			self._rbOffset = RbOffsetCls(self._core, self._cmd_group)
		return self._rbOffset

	@property
	def rsequence(self):
		"""rsequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsequence'):
			from .Rsequence import RsequenceCls
			self._rsequence = RsequenceCls(self._core, self._cmd_group)
		return self._rsequence

	@property
	def sindex(self):
		"""sindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sindex'):
			from .Sindex import SindexCls
			self._sindex = SindexCls(self._core, self._cmd_group)
		return self._sindex

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'SubfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
