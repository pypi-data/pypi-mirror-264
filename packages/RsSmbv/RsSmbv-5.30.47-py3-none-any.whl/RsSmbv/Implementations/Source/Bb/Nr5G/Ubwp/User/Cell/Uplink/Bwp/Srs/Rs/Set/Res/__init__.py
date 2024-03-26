from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal.RepeatedCapability import RepeatedCapability
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ResCls:
	"""Res commands group definition. 24 total commands, 18 Subgroups, 0 group commands
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
	def bhop(self):
		"""bhop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bhop'):
			from .Bhop import BhopCls
			self._bhop = BhopCls(self._core, self._cmd_group)
		return self._bhop

	@property
	def bsrs(self):
		"""bsrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bsrs'):
			from .Bsrs import BsrsCls
			self._bsrs = BsrsCls(self._core, self._cmd_group)
		return self._bsrs

	@property
	def coffset(self):
		"""coffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coffset'):
			from .Coffset import CoffsetCls
			self._coffset = CoffsetCls(self._core, self._cmd_group)
		return self._coffset

	@property
	def csrs(self):
		"""csrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csrs'):
			from .Csrs import CsrsCls
			self._csrs = CsrsCls(self._core, self._cmd_group)
		return self._csrs

	@property
	def fpos(self):
		"""fpos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fpos'):
			from .Fpos import FposCls
			self._fpos = FposCls(self._core, self._cmd_group)
		return self._fpos

	@property
	def fqShift(self):
		"""fqShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fqShift'):
			from .FqShift import FqShiftCls
			self._fqShift = FqShiftCls(self._core, self._cmd_group)
		return self._fqShift

	@property
	def fs(self):
		"""fs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fs'):
			from .Fs import FsCls
			self._fs = FsCls(self._core, self._cmd_group)
		return self._fs

	@property
	def naPort(self):
		"""naPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naPort'):
			from .NaPort import NaPortCls
			self._naPort = NaPortCls(self._core, self._cmd_group)
		return self._naPort

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
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def ptrs(self):
		"""ptrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptrs'):
			from .Ptrs import PtrsCls
			self._ptrs = PtrsCls(self._core, self._cmd_group)
		return self._ptrs

	@property
	def refactor(self):
		"""refactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_refactor'):
			from .Refactor import RefactorCls
			self._refactor = RefactorCls(self._core, self._cmd_group)
		return self._refactor

	@property
	def seq(self):
		"""seq commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_seq'):
			from .Seq import SeqCls
			self._seq = SeqCls(self._core, self._cmd_group)
		return self._seq

	@property
	def spos(self):
		"""spos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spos'):
			from .Spos import SposCls
			self._spos = SposCls(self._core, self._cmd_group)
		return self._spos

	@property
	def symNumber(self):
		"""symNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symNumber'):
			from .SymNumber import SymNumberCls
			self._symNumber = SymNumberCls(self._core, self._cmd_group)
		return self._symNumber

	@property
	def trtComb(self):
		"""trtComb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trtComb'):
			from .TrtComb import TrtCombCls
			self._trtComb = TrtCombCls(self._core, self._cmd_group)
		return self._trtComb

	def clone(self) -> 'ResCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ResCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
