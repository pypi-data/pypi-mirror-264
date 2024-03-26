from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlCls:
	"""Sl commands group definition. 89 total commands, 16 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sl", core, parent)

	@property
	def alloc(self):
		"""alloc commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .Alloc import AllocCls
			self._alloc = AllocCls(self._core, self._cmd_group)
		return self._alloc

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Dselect import DselectCls
			self._dselect = DselectCls(self._core, self._cmd_group)
		return self._dselect

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def nalloc(self):
		"""nalloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nalloc'):
			from .Nalloc import NallocCls
			self._nalloc = NallocCls(self._core, self._cmd_group)
		return self._nalloc

	@property
	def nsci(self):
		"""nsci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsci'):
			from .Nsci import NsciCls
			self._nsci = NsciCls(self._core, self._cmd_group)
		return self._nsci

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def rctrl(self):
		"""rctrl commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rctrl'):
			from .Rctrl import RctrlCls
			self._rctrl = RctrlCls(self._core, self._cmd_group)
		return self._rctrl

	@property
	def rdata(self):
		"""rdata commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_rdata'):
			from .Rdata import RdataCls
			self._rdata = RdataCls(self._core, self._cmd_group)
		return self._rdata

	@property
	def rdisc(self):
		"""rdisc commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_rdisc'):
			from .Rdisc import RdiscCls
			self._rdisc = RdiscCls(self._core, self._cmd_group)
		return self._rdisc

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restart'):
			from .Restart import RestartCls
			self._restart = RestartCls(self._core, self._cmd_group)
		return self._restart

	@property
	def rmc(self):
		"""rmc commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rmc'):
			from .Rmc import RmcCls
			self._rmc = RmcCls(self._core, self._cmd_group)
		return self._rmc

	@property
	def sci(self):
		"""sci commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_sci'):
			from .Sci import SciCls
			self._sci = SciCls(self._core, self._cmd_group)
		return self._sci

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def sync(self):
		"""sync commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Sync import SyncCls
			self._sync = SyncCls(self._core, self._cmd_group)
		return self._sync

	@property
	def v2X(self):
		"""v2X commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_v2X'):
			from .V2X import V2XCls
			self._v2X = V2XCls(self._core, self._cmd_group)
		return self._v2X

	def clone(self) -> 'SlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
