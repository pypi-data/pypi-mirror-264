from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SciCls:
	"""Sci commands group definition. 22 total commands, 22 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sci", core, parent)

	@property
	def amcsInd(self):
		"""amcsInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amcsInd'):
			from .AmcsInd import AmcsIndCls
			self._amcsInd = AmcsIndCls(self._core, self._cmd_group)
		return self._amcsInd

	@property
	def boind(self):
		"""boind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_boind'):
			from .Boind import BoindCls
			self._boind = BoindCls(self._core, self._cmd_group)
		return self._boind

	@property
	def correq(self):
		"""correq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_correq'):
			from .Correq import CorreqCls
			self._correq = CorreqCls(self._core, self._cmd_group)
		return self._correq

	@property
	def csiReq(self):
		"""csiReq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiReq'):
			from .CsiReq import CsiReqCls
			self._csiReq = CsiReqCls(self._core, self._cmd_group)
		return self._csiReq

	@property
	def ctInd(self):
		"""ctInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctInd'):
			from .CtInd import CtIndCls
			self._ctInd = CtIndCls(self._core, self._cmd_group)
		return self._ctInd

	@property
	def destId(self):
		"""destId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_destId'):
			from .DestId import DestIdCls
			self._destId = DestIdCls(self._core, self._cmd_group)
		return self._destId

	@property
	def dpatterns(self):
		"""dpatterns commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpatterns'):
			from .Dpatterns import DpatternsCls
			self._dpatterns = DpatternsCls(self._core, self._cmd_group)
		return self._dpatterns

	@property
	def dports(self):
		"""dports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dports'):
			from .Dports import DportsCls
			self._dports = DportsCls(self._core, self._cmd_group)
		return self._dports

	@property
	def frdRes(self):
		"""frdRes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frdRes'):
			from .FrdRes import FrdResCls
			self._frdRes = FrdResCls(self._core, self._cmd_group)
		return self._frdRes

	@property
	def harfb(self):
		"""harfb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harfb'):
			from .Harfb import HarfbCls
			self._harfb = HarfbCls(self._core, self._cmd_group)
		return self._harfb

	@property
	def harProc(self):
		"""harProc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harProc'):
			from .HarProc import HarProcCls
			self._harProc = HarProcCls(self._core, self._cmd_group)
		return self._harProc

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Mcs import McsCls
			self._mcs = McsCls(self._core, self._cmd_group)
		return self._mcs

	@property
	def ndi(self):
		"""ndi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndi'):
			from .Ndi import NdiCls
			self._ndi = NdiCls(self._core, self._cmd_group)
		return self._ndi

	@property
	def pfOverhead(self):
		"""pfOverhead commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfOverhead'):
			from .PfOverhead import PfOverheadCls
			self._pfOverhead = PfOverheadCls(self._core, self._cmd_group)
		return self._pfOverhead

	@property
	def prty(self):
		"""prty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prty'):
			from .Prty import PrtyCls
			self._prty = PrtyCls(self._core, self._cmd_group)
		return self._prty

	@property
	def redundancy(self):
		"""redundancy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_redundancy'):
			from .Redundancy import RedundancyCls
			self._redundancy = RedundancyCls(self._core, self._cmd_group)
		return self._redundancy

	@property
	def resved(self):
		"""resved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resved'):
			from .Resved import ResvedCls
			self._resved = ResvedCls(self._core, self._cmd_group)
		return self._resved

	@property
	def rrePeriod(self):
		"""rrePeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rrePeriod'):
			from .RrePeriod import RrePeriodCls
			self._rrePeriod = RrePeriodCls(self._core, self._cmd_group)
		return self._rrePeriod

	@property
	def s2Fmt(self):
		"""s2Fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_s2Fmt'):
			from .S2Fmt import S2FmtCls
			self._s2Fmt = S2FmtCls(self._core, self._cmd_group)
		return self._s2Fmt

	@property
	def sourId(self):
		"""sourId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sourId'):
			from .SourId import SourIdCls
			self._sourId = SourIdCls(self._core, self._cmd_group)
		return self._sourId

	@property
	def tidRes(self):
		"""tidRes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tidRes'):
			from .TidRes import TidResCls
			self._tidRes = TidResCls(self._core, self._cmd_group)
		return self._tidRes

	@property
	def zoneId(self):
		"""zoneId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zoneId'):
			from .ZoneId import ZoneIdCls
			self._zoneId = ZoneIdCls(self._core, self._cmd_group)
		return self._zoneId

	def clone(self) -> 'SciCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SciCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
