from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllocCls:
	"""Alloc commands group definition. 11 total commands, 11 Subgroups, 0 group commands
	Repeated Capability: AllocationNull, default value after init: AllocationNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alloc", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_allocationNull_get', 'repcap_allocationNull_set', repcap.AllocationNull.Nr0)

	def repcap_allocationNull_set(self, allocationNull: repcap.AllocationNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AllocationNull.Default
		Default value after init: AllocationNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(allocationNull)

	def repcap_allocationNull_get(self) -> repcap.AllocationNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def content(self):
		"""content commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_content'):
			from .Content import ContentCls
			self._content = ContentCls(self._core, self._cmd_group)
		return self._content

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def period(self):
		"""period commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_period'):
			from .Period import PeriodCls
			self._period = PeriodCls(self._core, self._cmd_group)
		return self._period

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .RbNumber import RbNumberCls
			self._rbNumber = RbNumberCls(self._core, self._cmd_group)
		return self._rbNumber

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .RbOffset import RbOffsetCls
			self._rbOffset = RbOffsetCls(self._core, self._cmd_group)
		return self._rbOffset

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetitions'):
			from .Repetitions import RepetitionsCls
			self._repetitions = RepetitionsCls(self._core, self._cmd_group)
		return self._repetitions

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .ScSpacing import ScSpacingCls
			self._scSpacing = ScSpacingCls(self._core, self._cmd_group)
		return self._scSpacing

	@property
	def slot(self):
		"""slot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slot'):
			from .Slot import SlotCls
			self._slot = SlotCls(self._core, self._cmd_group)
		return self._slot

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def symNumber(self):
		"""symNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symNumber'):
			from .SymNumber import SymNumberCls
			self._symNumber = SymNumberCls(self._core, self._cmd_group)
		return self._symNumber

	@property
	def symOffset(self):
		"""symOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symOffset'):
			from .SymOffset import SymOffsetCls
			self._symOffset = SymOffsetCls(self._core, self._cmd_group)
		return self._symOffset

	def clone(self) -> 'AllocCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AllocCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
