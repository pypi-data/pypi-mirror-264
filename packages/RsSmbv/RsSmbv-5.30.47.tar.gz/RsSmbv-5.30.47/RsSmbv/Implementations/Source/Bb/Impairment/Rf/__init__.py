from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfCls:
	"""Rf commands group definition. 8 total commands, 7 Subgroups, 0 group commands
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
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def iqRatio(self):
		"""iqRatio commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqRatio'):
			from .IqRatio import IqRatioCls
			self._iqRatio = IqRatioCls(self._core, self._cmd_group)
		return self._iqRatio

	@property
	def leakage(self):
		"""leakage commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_leakage'):
			from .Leakage import LeakageCls
			self._leakage = LeakageCls(self._core, self._cmd_group)
		return self._leakage

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Poffset import PoffsetCls
			self._poffset = PoffsetCls(self._core, self._cmd_group)
		return self._poffset

	@property
	def quadrature(self):
		"""quadrature commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_quadrature'):
			from .Quadrature import QuadratureCls
			self._quadrature = QuadratureCls(self._core, self._cmd_group)
		return self._quadrature

	@property
	def skew(self):
		"""skew commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_skew'):
			from .Skew import SkewCls
			self._skew = SkewCls(self._core, self._cmd_group)
		return self._skew

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'RfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
