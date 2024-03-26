from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 8 total commands, 8 Subgroups, 0 group commands
	Repeated Capability: Output, default value after init: Output.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_output_get', 'repcap_output_set', repcap.Output.Nr1)

	def repcap_output_set(self, output: repcap.Output) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Output.Default
		Default value after init: Output.Nr1"""
		self._cmd_group.set_repcap_enum_value(output)

	def repcap_output_get(self) -> repcap.Output:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def dinSec(self):
		"""dinSec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dinSec'):
			from .DinSec import DinSecCls
			self._dinSec = DinSecCls(self._core, self._cmd_group)
		return self._dinSec

	@property
	def foffset(self):
		"""foffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_foffset'):
			from .Foffset import FoffsetCls
			self._foffset = FoffsetCls(self._core, self._cmd_group)
		return self._foffset

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def offTime(self):
		"""offTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offTime'):
			from .OffTime import OffTimeCls
			self._offTime = OffTimeCls(self._core, self._cmd_group)
		return self._offTime

	@property
	def ontime(self):
		"""ontime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ontime'):
			from .Ontime import OntimeCls
			self._ontime = OntimeCls(self._core, self._cmd_group)
		return self._ontime

	@property
	def period(self):
		"""period commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_period'):
			from .Period import PeriodCls
			self._period = PeriodCls(self._core, self._cmd_group)
		return self._period

	@property
	def roffset(self):
		"""roffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_roffset'):
			from .Roffset import RoffsetCls
			self._roffset = RoffsetCls(self._core, self._cmd_group)
		return self._roffset

	def clone(self) -> 'OutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
