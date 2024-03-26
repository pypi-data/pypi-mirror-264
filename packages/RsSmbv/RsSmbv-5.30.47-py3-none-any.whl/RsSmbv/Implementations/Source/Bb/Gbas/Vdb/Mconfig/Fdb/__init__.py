from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdbCls:
	"""Fdb commands group definition. 15 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: FdbTransmitter, default value after init: FdbTransmitter.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdb", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_fdbTransmitter_get', 'repcap_fdbTransmitter_set', repcap.FdbTransmitter.Nr1)

	def repcap_fdbTransmitter_set(self, fdbTransmitter: repcap.FdbTransmitter) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FdbTransmitter.Default
		Default value after init: FdbTransmitter.Nr1"""
		self._cmd_group.set_repcap_enum_value(fdbTransmitter)

	def repcap_fdbTransmitter_get(self) -> repcap.FdbTransmitter:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def aid(self):
		"""aid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aid'):
			from .Aid import AidCls
			self._aid = AidCls(self._core, self._cmd_group)
		return self._aid

	@property
	def atcHeight(self):
		"""atcHeight commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atcHeight'):
			from .AtcHeight import AtcHeightCls
			self._atcHeight = AtcHeightCls(self._core, self._cmd_group)
		return self._atcHeight

	@property
	def ddlocation(self):
		"""ddlocation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ddlocation'):
			from .Ddlocation import DdlocationCls
			self._ddlocation = DdlocationCls(self._core, self._cmd_group)
		return self._ddlocation

	@property
	def dpLocation(self):
		"""dpLocation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpLocation'):
			from .DpLocation import DpLocationCls
			self._dpLocation = DpLocationCls(self._core, self._cmd_group)
		return self._dpLocation

	@property
	def gpAngle(self):
		"""gpAngle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gpAngle'):
			from .GpAngle import GpAngleCls
			self._gpAngle = GpAngleCls(self._core, self._cmd_group)
		return self._gpAngle

	@property
	def rletter(self):
		"""rletter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rletter'):
			from .Rletter import RletterCls
			self._rletter = RletterCls(self._core, self._cmd_group)
		return self._rletter

	@property
	def rnumber(self):
		"""rnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rnumber'):
			from .Rnumber import RnumberCls
			self._rnumber = RnumberCls(self._core, self._cmd_group)
		return self._rnumber

	@property
	def rpdf(self):
		"""rpdf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpdf'):
			from .Rpdf import RpdfCls
			self._rpdf = RpdfCls(self._core, self._cmd_group)
		return self._rpdf

	@property
	def rpif(self):
		"""rpif commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpif'):
			from .Rpif import RpifCls
			self._rpif = RpifCls(self._core, self._cmd_group)
		return self._rpif

	@property
	def ruIndicator(self):
		"""ruIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruIndicator'):
			from .RuIndicator import RuIndicatorCls
			self._ruIndicator = RuIndicatorCls(self._core, self._cmd_group)
		return self._ruIndicator

	def clone(self) -> 'FdbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FdbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
