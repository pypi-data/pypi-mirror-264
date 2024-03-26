from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsCls:
	"""Cs commands group definition. 295 total commands, 14 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cs", core, parent)

	@property
	def aulBwp(self):
		"""aulBwp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aulBwp'):
			from .AulBwp import AulBwpCls
			self._aulBwp = AulBwpCls(self._core, self._cmd_group)
		return self._aulBwp

	@property
	def dcces(self):
		"""dcces commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcces'):
			from .Dcces import DccesCls
			self._dcces = DccesCls(self._core, self._cmd_group)
		return self._dcces

	@property
	def dci(self):
		"""dci commands group. 268 Sub-classes, 0 commands."""
		if not hasattr(self, '_dci'):
			from .Dci import DciCls
			self._dci = DciCls(self._core, self._cmd_group)
		return self._dci

	@property
	def dmrs(self):
		"""dmrs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Dmrs import DmrsCls
			self._dmrs = DmrsCls(self._core, self._cmd_group)
		return self._dmrs

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def il(self):
		"""il commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_il'):
			from .Il import IlCls
			self._il = IlCls(self._core, self._cmd_group)
		return self._il

	@property
	def ndci(self):
		"""ndci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndci'):
			from .Ndci import NdciCls
			self._ndci = NdciCls(self._core, self._cmd_group)
		return self._ndci

	@property
	def nsci(self):
		"""nsci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsci'):
			from .Nsci import NsciCls
			self._nsci = NsciCls(self._core, self._cmd_group)
		return self._nsci

	@property
	def preGran(self):
		"""preGran commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preGran'):
			from .PreGran import PreGranCls
			self._preGran = PreGranCls(self._core, self._cmd_group)
		return self._preGran

	@property
	def puncturing(self):
		"""puncturing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_puncturing'):
			from .Puncturing import PuncturingCls
			self._puncturing = PuncturingCls(self._core, self._cmd_group)
		return self._puncturing

	@property
	def refDmrs(self):
		"""refDmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_refDmrs'):
			from .RefDmrs import RefDmrsCls
			self._refDmrs = RefDmrsCls(self._core, self._cmd_group)
		return self._refDmrs

	@property
	def resAlloc(self):
		"""resAlloc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_resAlloc'):
			from .ResAlloc import ResAllocCls
			self._resAlloc = ResAllocCls(self._core, self._cmd_group)
		return self._resAlloc

	@property
	def tci(self):
		"""tci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tci'):
			from .Tci import TciCls
			self._tci = TciCls(self._core, self._cmd_group)
		return self._tci

	@property
	def ts12(self):
		"""ts12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ts12'):
			from .Ts12 import Ts12Cls
			self._ts12 = Ts12Cls(self._core, self._cmd_group)
		return self._ts12

	def clone(self) -> 'CsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
