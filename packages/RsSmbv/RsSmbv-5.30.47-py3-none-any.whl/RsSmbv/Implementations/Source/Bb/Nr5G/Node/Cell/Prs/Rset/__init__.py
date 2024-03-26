from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsetCls:
	"""Rset commands group definition. 18 total commands, 9 Subgroups, 0 group commands
	Repeated Capability: ResourceSetNull, default value after init: ResourceSetNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rset", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_resourceSetNull_get', 'repcap_resourceSetNull_set', repcap.ResourceSetNull.Nr0)

	def repcap_resourceSetNull_set(self, resourceSetNull: repcap.ResourceSetNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ResourceSetNull.Default
		Default value after init: ResourceSetNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(resourceSetNull)

	def repcap_resourceSetNull_get(self) -> repcap.ResourceSetNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cmbSize(self):
		"""cmbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmbSize'):
			from .CmbSize import CmbSizeCls
			self._cmbSize = CmbSizeCls(self._core, self._cmd_group)
		return self._cmbSize

	@property
	def nresources(self):
		"""nresources commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nresources'):
			from .Nresources import NresourcesCls
			self._nresources = NresourcesCls(self._core, self._cmd_group)
		return self._nresources

	@property
	def per(self):
		"""per commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .Per import PerCls
			self._per = PerCls(self._core, self._cmd_group)
		return self._per

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .RbNumber import RbNumberCls
			self._rbNumber = RbNumberCls(self._core, self._cmd_group)
		return self._rbNumber

	@property
	def rbStart(self):
		"""rbStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbStart'):
			from .RbStart import RbStartCls
			self._rbStart = RbStartCls(self._core, self._cmd_group)
		return self._rbStart

	@property
	def repFactor(self):
		"""repFactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repFactor'):
			from .RepFactor import RepFactorCls
			self._repFactor = RepFactorCls(self._core, self._cmd_group)
		return self._repFactor

	@property
	def res(self):
		"""res commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_res'):
			from .Res import ResCls
			self._res = ResCls(self._core, self._cmd_group)
		return self._res

	@property
	def slOffset(self):
		"""slOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slOffset'):
			from .SlOffset import SlOffsetCls
			self._slOffset = SlOffsetCls(self._core, self._cmd_group)
		return self._slOffset

	@property
	def tgap(self):
		"""tgap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgap'):
			from .Tgap import TgapCls
			self._tgap = TgapCls(self._core, self._cmd_group)
		return self._tgap

	def clone(self) -> 'RsetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RsetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
