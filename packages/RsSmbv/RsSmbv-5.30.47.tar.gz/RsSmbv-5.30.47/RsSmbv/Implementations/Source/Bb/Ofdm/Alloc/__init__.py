from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllocCls:
	"""Alloc commands group definition. 33 total commands, 19 Subgroups, 0 group commands
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
	def ciqFile(self):
		"""ciqFile commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ciqFile'):
			from .CiqFile import CiqFileCls
			self._ciqFile = CiqFileCls(self._core, self._cmd_group)
		return self._ciqFile

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def conPoint(self):
		"""conPoint commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_conPoint'):
			from .ConPoint import ConPointCls
			self._conPoint = ConPointCls(self._core, self._cmd_group)
		return self._conPoint

	@property
	def content(self):
		"""content commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_content'):
			from .Content import ContentCls
			self._content = ContentCls(self._core, self._cmd_group)
		return self._content

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def moor(self):
		"""moor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_moor'):
			from .Moor import MoorCls
			self._moor = MoorCls(self._core, self._cmd_group)
		return self._moor

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .PhysBits import PhysBitsCls
			self._physBits = PhysBitsCls(self._core, self._cmd_group)
		return self._physBits

	@property
	def pwr(self):
		"""pwr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pwr'):
			from .Pwr import PwrCls
			self._pwr = PwrCls(self._core, self._cmd_group)
		return self._pwr

	@property
	def scma(self):
		"""scma commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_scma'):
			from .Scma import ScmaCls
			self._scma = ScmaCls(self._core, self._cmd_group)
		return self._scma

	@property
	def scno(self):
		"""scno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scno'):
			from .Scno import ScnoCls
			self._scno = ScnoCls(self._core, self._cmd_group)
		return self._scno

	@property
	def scOffset(self):
		"""scOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scOffset'):
			from .ScOffset import ScOffsetCls
			self._scOffset = ScOffsetCls(self._core, self._cmd_group)
		return self._scOffset

	@property
	def splt(self):
		"""splt commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_splt'):
			from .Splt import SpltCls
			self._splt = SpltCls(self._core, self._cmd_group)
		return self._splt

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def syno(self):
		"""syno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_syno'):
			from .Syno import SynoCls
			self._syno = SynoCls(self._core, self._cmd_group)
		return self._syno

	@property
	def syOffset(self):
		"""syOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_syOffset'):
			from .SyOffset import SyOffsetCls
			self._syOffset = SyOffsetCls(self._core, self._cmd_group)
		return self._syOffset

	@property
	def zad(self):
		"""zad commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_zad'):
			from .Zad import ZadCls
			self._zad = ZadCls(self._core, self._cmd_group)
		return self._zad

	def clone(self) -> 'AllocCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AllocCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
