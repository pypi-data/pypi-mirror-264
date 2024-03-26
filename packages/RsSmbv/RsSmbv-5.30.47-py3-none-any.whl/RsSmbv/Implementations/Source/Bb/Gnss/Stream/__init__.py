from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StreamCls:
	"""Stream commands group definition. 15 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stream", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def repcap_stream_set(self, stream: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._cmd_group.set_repcap_enum_value(stream)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def antenna(self):
		"""antenna commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_antenna'):
			from .Antenna import AntennaCls
			self._antenna = AntennaCls(self._core, self._cmd_group)
		return self._antenna

	@property
	def bb(self):
		"""bb commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	@property
	def channels(self):
		"""channels commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channels'):
			from .Channels import ChannelsCls
			self._channels = ChannelsCls(self._core, self._cmd_group)
		return self._channels

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def l1Band(self):
		"""l1Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1Band'):
			from .L1Band import L1BandCls
			self._l1Band = L1BandCls(self._core, self._cmd_group)
		return self._l1Band

	@property
	def l2Band(self):
		"""l2Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l2Band'):
			from .L2Band import L2BandCls
			self._l2Band = L2BandCls(self._core, self._cmd_group)
		return self._l2Band

	@property
	def l5Band(self):
		"""l5Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l5Band'):
			from .L5Band import L5BandCls
			self._l5Band = L5BandCls(self._core, self._cmd_group)
		return self._l5Band

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def rfBand(self):
		"""rfBand commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfBand'):
			from .RfBand import RfBandCls
			self._rfBand = RfBandCls(self._core, self._cmd_group)
		return self._rfBand

	@property
	def vehicle(self):
		"""vehicle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vehicle'):
			from .Vehicle import VehicleCls
			self._vehicle = VehicleCls(self._core, self._cmd_group)
		return self._vehicle

	def clone(self) -> 'StreamCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StreamCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
