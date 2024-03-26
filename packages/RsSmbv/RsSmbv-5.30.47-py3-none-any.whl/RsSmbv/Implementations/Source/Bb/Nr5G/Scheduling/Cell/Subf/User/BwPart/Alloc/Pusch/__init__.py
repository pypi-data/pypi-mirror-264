from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschCls:
	"""Pusch commands group definition. 49 total commands, 14 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pusch", core, parent)

	@property
	def bmaid(self):
		"""bmaid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmaid'):
			from .Bmaid import BmaidCls
			self._bmaid = BmaidCls(self._core, self._cmd_group)
		return self._bmaid

	@property
	def dmr(self):
		"""dmr commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmr'):
			from .Dmr import DmrCls
			self._dmr = DmrCls(self._core, self._cmd_group)
		return self._dmr

	@property
	def dmrs(self):
		"""dmrs commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Dmrs import DmrsCls
			self._dmrs = DmrsCls(self._core, self._cmd_group)
		return self._dmrs

	@property
	def fhOi(self):
		"""fhOi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fhOi'):
			from .FhOi import FhOiCls
			self._fhOi = FhOiCls(self._core, self._cmd_group)
		return self._fhOi

	@property
	def fhop(self):
		"""fhop commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fhop'):
			from .Fhop import FhopCls
			self._fhop = FhopCls(self._core, self._cmd_group)
		return self._fhop

	@property
	def hprNumber(self):
		"""hprNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hprNumber'):
			from .HprNumber import HprNumberCls
			self._hprNumber = HprNumberCls(self._core, self._cmd_group)
		return self._hprNumber

	@property
	def int(self):
		"""int commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_int'):
			from .Int import IntCls
			self._int = IntCls(self._core, self._cmd_group)
		return self._int

	@property
	def nint(self):
		"""nint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nint'):
			from .Nint import NintCls
			self._nint = NintCls(self._core, self._cmd_group)
		return self._nint

	@property
	def ptrs(self):
		"""ptrs commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptrs'):
			from .Ptrs import PtrsCls
			self._ptrs = PtrsCls(self._core, self._cmd_group)
		return self._ptrs

	@property
	def resAlloc(self):
		"""resAlloc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_resAlloc'):
			from .ResAlloc import ResAllocCls
			self._resAlloc = ResAllocCls(self._core, self._cmd_group)
		return self._resAlloc

	@property
	def sint(self):
		"""sint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sint'):
			from .Sint import SintCls
			self._sint = SintCls(self._core, self._cmd_group)
		return self._sint

	@property
	def txScheme(self):
		"""txScheme commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_txScheme'):
			from .TxScheme import TxSchemeCls
			self._txScheme = TxSchemeCls(self._core, self._cmd_group)
		return self._txScheme

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def uci(self):
		"""uci commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_uci'):
			from .Uci import UciCls
			self._uci = UciCls(self._core, self._cmd_group)
		return self._uci

	def clone(self) -> 'PuschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PuschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
