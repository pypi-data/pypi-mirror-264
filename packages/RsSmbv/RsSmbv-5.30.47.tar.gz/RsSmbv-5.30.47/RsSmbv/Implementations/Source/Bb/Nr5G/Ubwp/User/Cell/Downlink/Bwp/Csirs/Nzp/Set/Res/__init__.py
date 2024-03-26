from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal.RepeatedCapability import RepeatedCapability
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ResCls:
	"""Res commands group definition. 17 total commands, 14 Subgroups, 0 group commands
	Repeated Capability: ResourceNull, default value after init: ResourceNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("res", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_resourceNull_get', 'repcap_resourceNull_set', repcap.ResourceNull.Nr0)

	def repcap_resourceNull_set(self, resourceNull: repcap.ResourceNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ResourceNull.Default
		Default value after init: ResourceNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(resourceNull)

	def repcap_resourceNull_get(self) -> repcap.ResourceNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def apMap(self):
		"""apMap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_apMap'):
			from .ApMap import ApMapCls
			self._apMap = ApMapCls(self._core, self._cmd_group)
		return self._apMap

	@property
	def bitmap(self):
		"""bitmap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitmap'):
			from .Bitmap import BitmapCls
			self._bitmap = BitmapCls(self._core, self._cmd_group)
		return self._bitmap

	@property
	def cdmType(self):
		"""cdmType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdmType'):
			from .CdmType import CdmTypeCls
			self._cdmType = CdmTypeCls(self._core, self._cmd_group)
		return self._cdmType

	@property
	def density(self):
		"""density commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_density'):
			from .Density import DensityCls
			self._density = DensityCls(self._core, self._cmd_group)
		return self._density

	@property
	def i0(self):
		"""i0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i0'):
			from .I0 import I0Cls
			self._i0 = I0Cls(self._core, self._cmd_group)
		return self._i0

	@property
	def i1(self):
		"""i1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i1'):
			from .I1 import I1Cls
			self._i1 = I1Cls(self._core, self._cmd_group)
		return self._i1

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def per(self):
		"""per commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_per'):
			from .Per import PerCls
			self._per = PerCls(self._core, self._cmd_group)
		return self._per

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .Ports import PortsCls
			self._ports = PortsCls(self._core, self._cmd_group)
		return self._ports

	@property
	def pwr(self):
		"""pwr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pwr'):
			from .Pwr import PwrCls
			self._pwr = PwrCls(self._core, self._cmd_group)
		return self._pwr

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .RbNumber import RbNumberCls
			self._rbNumber = RbNumberCls(self._core, self._cmd_group)
		return self._rbNumber

	@property
	def row(self):
		"""row commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	@property
	def scid(self):
		"""scid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scid'):
			from .Scid import ScidCls
			self._scid = ScidCls(self._core, self._cmd_group)
		return self._scid

	@property
	def srbNumber(self):
		"""srbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srbNumber'):
			from .SrbNumber import SrbNumberCls
			self._srbNumber = SrbNumberCls(self._core, self._cmd_group)
		return self._srbNumber

	def clone(self) -> 'ResCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ResCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
