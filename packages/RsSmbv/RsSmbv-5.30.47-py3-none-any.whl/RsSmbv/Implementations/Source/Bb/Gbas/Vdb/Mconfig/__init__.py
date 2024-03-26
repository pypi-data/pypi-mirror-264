from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MconfigCls:
	"""Mconfig commands group definition. 101 total commands, 54 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mconfig", core, parent)

	@property
	def adb1(self):
		"""adb1 commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adb1'):
			from .Adb1 import Adb1Cls
			self._adb1 = Adb1Cls(self._core, self._cmd_group)
		return self._adb1

	@property
	def adb3(self):
		"""adb3 commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adb3'):
			from .Adb3 import Adb3Cls
			self._adb3 = Adb3Cls(self._core, self._cmd_group)
		return self._adb3

	@property
	def adb4(self):
		"""adb4 commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adb4'):
			from .Adb4 import Adb4Cls
			self._adb4 = Adb4Cls(self._core, self._cmd_group)
		return self._adb4

	@property
	def aid(self):
		"""aid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aid'):
			from .Aid import AidCls
			self._aid = AidCls(self._core, self._cmd_group)
		return self._aid

	@property
	def apDesignator(self):
		"""apDesignator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apDesignator'):
			from .ApDesignator import ApDesignatorCls
			self._apDesignator = ApDesignatorCls(self._core, self._cmd_group)
		return self._apDesignator

	@property
	def atcHeight(self):
		"""atcHeight commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atcHeight'):
			from .AtcHeight import AtcHeightCls
			self._atcHeight = AtcHeightCls(self._core, self._cmd_group)
		return self._atcHeight

	@property
	def atuSelector(self):
		"""atuSelector commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atuSelector'):
			from .AtuSelector import AtuSelectorCls
			self._atuSelector = AtuSelectorCls(self._core, self._cmd_group)
		return self._atuSelector

	@property
	def cwaThreshold(self):
		"""cwaThreshold commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cwaThreshold'):
			from .CwaThreshold import CwaThresholdCls
			self._cwaThreshold = CwaThresholdCls(self._core, self._cmd_group)
		return self._cwaThreshold

	@property
	def dfLocation(self):
		"""dfLocation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dfLocation'):
			from .DfLocation import DfLocationCls
			self._dfLocation = DfLocationCls(self._core, self._cmd_group)
		return self._dfLocation

	@property
	def dg(self):
		"""dg commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_dg'):
			from .Dg import DgCls
			self._dg = DgCls(self._core, self._cmd_group)
		return self._dg

	@property
	def dlOffset(self):
		"""dlOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlOffset'):
			from .DlOffset import DlOffsetCls
			self._dlOffset = DlOffsetCls(self._core, self._cmd_group)
		return self._dlOffset

	@property
	def fdb(self):
		"""fdb commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdb'):
			from .Fdb import FdbCls
			self._fdb = FdbCls(self._core, self._cmd_group)
		return self._fdb

	@property
	def fdBlock(self):
		"""fdBlock commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdBlock'):
			from .FdBlock import FdBlockCls
			self._fdBlock = FdBlockCls(self._core, self._cmd_group)
		return self._fdBlock

	@property
	def fdsState(self):
		"""fdsState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdsState'):
			from .FdsState import FdsStateCls
			self._fdsState = FdsStateCls(self._core, self._cmd_group)
		return self._fdsState

	@property
	def flaa(self):
		"""flaa commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_flaa'):
			from .Flaa import FlaaCls
			self._flaa = FlaaCls(self._core, self._cmd_group)
		return self._flaa

	@property
	def frcLink(self):
		"""frcLink commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frcLink'):
			from .FrcLink import FrcLinkCls
			self._frcLink = FrcLinkCls(self._core, self._cmd_group)
		return self._frcLink

	@property
	def fvaa(self):
		"""fvaa commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fvaa'):
			from .Fvaa import FvaaCls
			self._fvaa = FvaaCls(self._core, self._cmd_group)
		return self._fvaa

	@property
	def gcid(self):
		"""gcid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gcid'):
			from .Gcid import GcidCls
			self._gcid = GcidCls(self._core, self._cmd_group)
		return self._gcid

	@property
	def gpAngle(self):
		"""gpAngle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gpAngle'):
			from .GpAngle import GpAngleCls
			self._gpAngle = GpAngleCls(self._core, self._cmd_group)
		return self._gpAngle

	@property
	def gsaDesignator(self):
		"""gsaDesignator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gsaDesignator'):
			from .GsaDesignator import GsaDesignatorCls
			self._gsaDesignator = GsaDesignatorCls(self._core, self._cmd_group)
		return self._gsaDesignator

	@property
	def gsrReceivers(self):
		"""gsrReceivers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gsrReceivers'):
			from .GsrReceivers import GsrReceiversCls
			self._gsrReceivers = GsrReceiversCls(self._core, self._cmd_group)
		return self._gsrReceivers

	@property
	def kcGlonass(self):
		"""kcGlonass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kcGlonass'):
			from .KcGlonass import KcGlonassCls
			self._kcGlonass = KcGlonassCls(self._core, self._cmd_group)
		return self._kcGlonass

	@property
	def kcGps(self):
		"""kcGps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kcGps'):
			from .KcGps import KcGpsCls
			self._kcGps = KcGpsCls(self._core, self._cmd_group)
		return self._kcGps

	@property
	def kdGlonass(self):
		"""kdGlonass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kdGlonass'):
			from .KdGlonass import KdGlonassCls
			self._kdGlonass = KdGlonassCls(self._core, self._cmd_group)
		return self._kdGlonass

	@property
	def kdGps(self):
		"""kdGps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kdGps'):
			from .KdGps import KdGpsCls
			self._kdGps = KdGpsCls(self._core, self._cmd_group)
		return self._kdGps

	@property
	def kpGlonass(self):
		"""kpGlonass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kpGlonass'):
			from .KpGlonass import KpGlonassCls
			self._kpGlonass = KpGlonassCls(self._core, self._cmd_group)
		return self._kpGlonass

	@property
	def kpGps(self):
		"""kpGps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kpGps'):
			from .KpGps import KpGpsCls
			self._kpGps = KpGpsCls(self._core, self._cmd_group)
		return self._kpGps

	@property
	def lfLocation(self):
		"""lfLocation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_lfLocation'):
			from .LfLocation import LfLocationCls
			self._lfLocation = LfLocationCls(self._core, self._cmd_group)
		return self._lfLocation

	@property
	def lmVariation(self):
		"""lmVariation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lmVariation'):
			from .LmVariation import LmVariationCls
			self._lmVariation = LmVariationCls(self._core, self._cmd_group)
		return self._lmVariation

	@property
	def location(self):
		"""location commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_location'):
			from .Location import LocationCls
			self._location = LocationCls(self._core, self._cmd_group)
		return self._location

	@property
	def mt2State(self):
		"""mt2State commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mt2State'):
			from .Mt2State import Mt2StateCls
			self._mt2State = Mt2StateCls(self._core, self._cmd_group)
		return self._mt2State

	@property
	def mt4State(self):
		"""mt4State commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mt4State'):
			from .Mt4State import Mt4StateCls
			self._mt4State = Mt4StateCls(self._core, self._cmd_group)
		return self._mt4State

	@property
	def muDistance(self):
		"""muDistance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_muDistance'):
			from .MuDistance import MuDistanceCls
			self._muDistance = MuDistanceCls(self._core, self._cmd_group)
		return self._muDistance

	@property
	def nfdBlocks(self):
		"""nfdBlocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nfdBlocks'):
			from .NfdBlocks import NfdBlocksCls
			self._nfdBlocks = NfdBlocksCls(self._core, self._cmd_group)
		return self._nfdBlocks

	@property
	def nopPoint(self):
		"""nopPoint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nopPoint'):
			from .NopPoint import NopPointCls
			self._nopPoint = NopPointCls(self._core, self._cmd_group)
		return self._nopPoint

	@property
	def pservice(self):
		"""pservice commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pservice'):
			from .Pservice import PserviceCls
			self._pservice = PserviceCls(self._core, self._cmd_group)
		return self._pservice

	@property
	def rfIndex(self):
		"""rfIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfIndex'):
			from .RfIndex import RfIndexCls
			self._rfIndex = RfIndexCls(self._core, self._cmd_group)
		return self._rfIndex

	@property
	def rletter(self):
		"""rletter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rletter'):
			from .Rletter import RletterCls
			self._rletter = RletterCls(self._core, self._cmd_group)
		return self._rletter

	@property
	def rnumber(self):
		"""rnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rnumber'):
			from .Rnumber import RnumberCls
			self._rnumber = RnumberCls(self._core, self._cmd_group)
		return self._rnumber

	@property
	def rpdf(self):
		"""rpdf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpdf'):
			from .Rpdf import RpdfCls
			self._rpdf = RpdfCls(self._core, self._cmd_group)
		return self._rpdf

	@property
	def rpdt(self):
		"""rpdt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpdt'):
			from .Rpdt import RpdtCls
			self._rpdt = RpdtCls(self._core, self._cmd_group)
		return self._rpdt

	@property
	def rpif(self):
		"""rpif commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpif'):
			from .Rpif import RpifCls
			self._rpif = RpifCls(self._core, self._cmd_group)
		return self._rpif

	@property
	def rpit(self):
		"""rpit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpit'):
			from .Rpit import RpitCls
			self._rpit = RpitCls(self._core, self._cmd_group)
		return self._rpit

	@property
	def rsdSelector(self):
		"""rsdSelector commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsdSelector'):
			from .RsdSelector import RsdSelectorCls
			self._rsdSelector = RsdSelectorCls(self._core, self._cmd_group)
		return self._rsdSelector

	@property
	def ruIndicator(self):
		"""ruIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruIndicator'):
			from .RuIndicator import RuIndicatorCls
			self._ruIndicator = RuIndicatorCls(self._core, self._cmd_group)
		return self._ruIndicator

	@property
	def runcertainty(self):
		"""runcertainty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_runcertainty'):
			from .Runcertainty import RuncertaintyCls
			self._runcertainty = RuncertaintyCls(self._core, self._cmd_group)
		return self._runcertainty

	@property
	def sgDefinition(self):
		"""sgDefinition commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_sgDefinition'):
			from .SgDefinition import SgDefinitionCls
			self._sgDefinition = SgDefinitionCls(self._core, self._cmd_group)
		return self._sgDefinition

	@property
	def sheight(self):
		"""sheight commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sheight'):
			from .Sheight import SheightCls
			self._sheight = SheightCls(self._core, self._cmd_group)
		return self._sheight

	@property
	def svid(self):
		"""svid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_svid'):
			from .Svid import SvidCls
			self._svid = SvidCls(self._core, self._cmd_group)
		return self._svid

	@property
	def sviGradient(self):
		"""sviGradient commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sviGradient'):
			from .SviGradient import SviGradientCls
			self._sviGradient = SviGradientCls(self._core, self._cmd_group)
		return self._sviGradient

	@property
	def tdsState(self):
		"""tdsState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdsState'):
			from .TdsState import TdsStateCls
			self._tdsState = TdsStateCls(self._core, self._cmd_group)
		return self._tdsState

	@property
	def tlas(self):
		"""tlas commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tlas'):
			from .Tlas import TlasCls
			self._tlas = TlasCls(self._core, self._cmd_group)
		return self._tlas

	@property
	def tvas(self):
		"""tvas commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tvas'):
			from .Tvas import TvasCls
			self._tvas = TvasCls(self._core, self._cmd_group)
		return self._tvas

	@property
	def waypoint(self):
		"""waypoint commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_waypoint'):
			from .Waypoint import WaypointCls
			self._waypoint = WaypointCls(self._core, self._cmd_group)
		return self._waypoint

	def clone(self) -> 'MconfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MconfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
