from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CellCls:
	"""Cell commands group definition. 16 total commands, 9 Subgroups, 0 group commands
	Repeated Capability: CellNull, default value after init: CellNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cell", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_cellNull_get', 'repcap_cellNull_set', repcap.CellNull.Nr0)

	def repcap_cellNull_set(self, cellNull: repcap.CellNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CellNull.Default
		Default value after init: CellNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(cellNull)

	def repcap_cellNull_get(self) -> repcap.CellNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cdState(self):
		"""cdState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdState'):
			from .CdState import CdStateCls
			self._cdState = CdStateCls(self._core, self._cmd_group)
		return self._cdState

	@property
	def csirs(self):
		"""csirs commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_csirs'):
			from .Csirs import CsirsCls
			self._csirs = CsirsCls(self._core, self._cmd_group)
		return self._csirs

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def nzpNum(self):
		"""nzpNum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzpNum'):
			from .NzpNum import NzpNumCls
			self._nzpNum = NzpNumCls(self._core, self._cmd_group)
		return self._nzpNum

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def periodicity(self):
		"""periodicity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_periodicity'):
			from .Periodicity import PeriodicityCls
			self._periodicity = PeriodicityCls(self._core, self._cmd_group)
		return self._periodicity

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def zpNum(self):
		"""zpNum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpNum'):
			from .ZpNum import ZpNumCls
			self._zpNum = ZpNumCls(self._core, self._cmd_group)
		return self._zpNum

	def clone(self) -> 'CellCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CellCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
