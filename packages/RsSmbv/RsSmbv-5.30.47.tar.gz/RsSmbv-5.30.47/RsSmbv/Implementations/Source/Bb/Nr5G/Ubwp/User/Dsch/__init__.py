from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DschCls:
	"""Dsch commands group definition. 19 total commands, 19 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dsch", core, parent)

	@property
	def anfMode(self):
		"""anfMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anfMode'):
			from .AnfMode import AnfModeCls
			self._anfMode = AnfModeCls(self._core, self._cmd_group)
		return self._anfMode

	@property
	def ccoding(self):
		"""ccoding commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Ccoding import CcodingCls
			self._ccoding = CcodingCls(self._core, self._cmd_group)
		return self._ccoding

	@property
	def cdin(self):
		"""cdin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdin'):
			from .Cdin import CdinCls
			self._cdin = CdinCls(self._core, self._cmd_group)
		return self._cdin

	@property
	def cods(self):
		"""cods commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cods'):
			from .Cods import CodsCls
			self._cods = CodsCls(self._core, self._cmd_group)
		return self._cods

	@property
	def da02(self):
		"""da02 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_da02'):
			from .Da02 import Da02Cls
			self._da02 = Da02Cls(self._core, self._cmd_group)
		return self._da02

	@property
	def dait(self):
		"""dait commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dait'):
			from .Dait import DaitCls
			self._dait = DaitCls(self._core, self._cmd_group)
		return self._dait

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def daul(self):
		"""daul commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_daul'):
			from .Daul import DaulCls
			self._daul = DaulCls(self._core, self._cmd_group)
		return self._daul

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .Dlist import DlistCls
			self._dlist = DlistCls(self._core, self._cmd_group)
		return self._dlist

	@property
	def hartInd(self):
		"""hartInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hartInd'):
			from .HartInd import HartIndCls
			self._hartInd = HartIndCls(self._core, self._cmd_group)
		return self._hartInd

	@property
	def initPattern(self):
		"""initPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_initPattern'):
			from .InitPattern import InitPatternCls
			self._initPattern = InitPatternCls(self._core, self._cmd_group)
		return self._initPattern

	@property
	def nrbs(self):
		"""nrbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrbs'):
			from .Nrbs import NrbsCls
			self._nrbs = NrbsCls(self._core, self._cmd_group)
		return self._nrbs

	@property
	def nssf(self):
		"""nssf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nssf'):
			from .Nssf import NssfCls
			self._nssf = NssfCls(self._core, self._cmd_group)
		return self._nssf

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def ph1F(self):
		"""ph1F commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ph1F'):
			from .Ph1F import Ph1FCls
			self._ph1F = Ph1FCls(self._core, self._cmd_group)
		return self._ph1F

	@property
	def psscDyn(self):
		"""psscDyn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psscDyn'):
			from .PsscDyn import PsscDynCls
			self._psscDyn = PsscDynCls(self._core, self._cmd_group)
		return self._psscDyn

	@property
	def rbis(self):
		"""rbis commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbis'):
			from .Rbis import RbisCls
			self._rbis = RbisCls(self._core, self._cmd_group)
		return self._rbis

	@property
	def scgw(self):
		"""scgw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scgw'):
			from .Scgw import ScgwCls
			self._scgw = ScgwCls(self._core, self._cmd_group)
		return self._scgw

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Scrambling import ScramblingCls
			self._scrambling = ScramblingCls(self._core, self._cmd_group)
		return self._scrambling

	def clone(self) -> 'DschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
