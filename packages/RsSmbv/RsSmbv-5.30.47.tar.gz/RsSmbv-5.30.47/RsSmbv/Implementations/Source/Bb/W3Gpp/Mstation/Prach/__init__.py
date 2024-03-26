from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrachCls:
	"""Prach commands group definition. 25 total commands, 15 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prach", core, parent)

	@property
	def aslot(self):
		"""aslot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aslot'):
			from .Aslot import AslotCls
			self._aslot = AslotCls(self._core, self._cmd_group)
		return self._aslot

	@property
	def atTiming(self):
		"""atTiming commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atTiming'):
			from .AtTiming import AtTimingCls
			self._atTiming = AtTimingCls(self._core, self._cmd_group)
		return self._atTiming

	@property
	def cpower(self):
		"""cpower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpower'):
			from .Cpower import CpowerCls
			self._cpower = CpowerCls(self._core, self._cmd_group)
		return self._cpower

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dpower(self):
		"""dpower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpower'):
			from .Dpower import DpowerCls
			self._dpower = DpowerCls(self._core, self._cmd_group)
		return self._dpower

	@property
	def mlength(self):
		"""mlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mlength'):
			from .Mlength import MlengthCls
			self._mlength = MlengthCls(self._core, self._cmd_group)
		return self._mlength

	@property
	def ppower(self):
		"""ppower commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ppower'):
			from .Ppower import PpowerCls
			self._ppower = PpowerCls(self._core, self._cmd_group)
		return self._ppower

	@property
	def prepetition(self):
		"""prepetition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prepetition'):
			from .Prepetition import PrepetitionCls
			self._prepetition = PrepetitionCls(self._core, self._cmd_group)
		return self._prepetition

	@property
	def rafter(self):
		"""rafter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rafter'):
			from .Rafter import RafterCls
			self._rafter = RafterCls(self._core, self._cmd_group)
		return self._rafter

	@property
	def rarb(self):
		"""rarb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rarb'):
			from .Rarb import RarbCls
			self._rarb = RarbCls(self._core, self._cmd_group)
		return self._rarb

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def signature(self):
		"""signature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_signature'):
			from .Signature import SignatureCls
			self._signature = SignatureCls(self._core, self._cmd_group)
		return self._signature

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def tfci(self):
		"""tfci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .Tfci import TfciCls
			self._tfci = TfciCls(self._core, self._cmd_group)
		return self._tfci

	@property
	def timing(self):
		"""timing commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_timing'):
			from .Timing import TimingCls
			self._timing = TimingCls(self._core, self._cmd_group)
		return self._timing

	def clone(self) -> 'PrachCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PrachCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
