from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllocCls:
	"""Alloc commands group definition. 534 total commands, 61 Subgroups, 0 group commands
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
	def agft(self):
		"""agft commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_agft'):
			from .Agft import AgftCls
			self._agft = AgftCls(self._core, self._cmd_group)
		return self._agft

	@property
	def agOffset(self):
		"""agOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_agOffset'):
			from .AgOffset import AgOffsetCls
			self._agOffset = AgOffsetCls(self._core, self._cmd_group)
		return self._agOffset

	@property
	def apMap(self):
		"""apMap commands group. 2 Sub-classes, 0 commands."""
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
	def bitmap(self):
		"""bitmap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitmap'):
			from .Bitmap import BitmapCls
			self._bitmap = BitmapCls(self._core, self._cmd_group)
		return self._bitmap

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
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Config import ConfigCls
			self._config = ConfigCls(self._core, self._cmd_group)
		return self._config

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def content(self):
		"""content commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_content'):
			from .Content import ContentCls
			self._content = ContentCls(self._core, self._cmd_group)
		return self._content

	@property
	def copyTo(self):
		"""copyTo commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_copyTo'):
			from .CopyTo import CopyToCls
			self._copyTo = CopyToCls(self._core, self._cmd_group)
		return self._copyTo

	@property
	def cpext(self):
		"""cpext commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpext'):
			from .Cpext import CpextCls
			self._cpext = CpextCls(self._core, self._cmd_group)
		return self._cpext

	@property
	def cs(self):
		"""cs commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_cs'):
			from .Cs import CsCls
			self._cs = CsCls(self._core, self._cmd_group)
		return self._cs

	@property
	def csrs(self):
		"""csrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csrs'):
			from .Csrs import CsrsCls
			self._csrs = CsrsCls(self._core, self._cmd_group)
		return self._csrs

	@property
	def density(self):
		"""density commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_density'):
			from .Density import DensityCls
			self._density = DensityCls(self._core, self._cmd_group)
		return self._density

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def facts(self):
		"""facts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_facts'):
			from .Facts import FactsCls
			self._facts = FactsCls(self._core, self._cmd_group)
		return self._facts

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Fmt import FmtCls
			self._fmt = FmtCls(self._core, self._cmd_group)
		return self._fmt

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
	def fsFactor(self):
		"""fsFactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fsFactor'):
			from .FsFactor import FsFactorCls
			self._fsFactor = FsFactorCls(self._core, self._cmd_group)
		return self._fsFactor

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
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def iszPower(self):
		"""iszPower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iszPower'):
			from .IszPower import IszPowerCls
			self._iszPower = IszPowerCls(self._core, self._cmd_group)
		return self._iszPower

	@property
	def mapType(self):
		"""mapType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapType'):
			from .MapType import MapTypeCls
			self._mapType = MapTypeCls(self._core, self._cmd_group)
		return self._mapType

	@property
	def nap(self):
		"""nap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nap'):
			from .Nap import NapCls
			self._nap = NapCls(self._core, self._cmd_group)
		return self._nap

	@property
	def ntbms(self):
		"""ntbms commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntbms'):
			from .Ntbms import NtbmsCls
			self._ntbms = NtbmsCls(self._core, self._cmd_group)
		return self._ntbms

	@property
	def pdsch(self):
		"""pdsch commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsch'):
			from .Pdsch import PdschCls
			self._pdsch = PdschCls(self._core, self._cmd_group)
		return self._pdsch

	@property
	def period(self):
		"""period commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_period'):
			from .Period import PeriodCls
			self._period = PeriodCls(self._core, self._cmd_group)
		return self._period

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .Ports import PortsCls
			self._ports = PortsCls(self._core, self._cmd_group)
		return self._ports

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def prach(self):
		"""prach commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_prach'):
			from .Prach import PrachCls
			self._prach = PrachCls(self._core, self._cmd_group)
		return self._prach

	@property
	def pscch(self):
		"""pscch commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pscch'):
			from .Pscch import PscchCls
			self._pscch = PscchCls(self._core, self._cmd_group)
		return self._pscch

	@property
	def psfch(self):
		"""psfch commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_psfch'):
			from .Psfch import PsfchCls
			self._psfch = PsfchCls(self._core, self._cmd_group)
		return self._psfch

	@property
	def pssch(self):
		"""pssch commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_pssch'):
			from .Pssch import PsschCls
			self._pssch = PsschCls(self._core, self._cmd_group)
		return self._pssch

	@property
	def pucch(self):
		"""pucch commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_pucch'):
			from .Pucch import PucchCls
			self._pucch = PucchCls(self._core, self._cmd_group)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	@property
	def rbNumber(self):
		"""rbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbNumber'):
			from .RbNumber import RbNumberCls
			self._rbNumber = RbNumberCls(self._core, self._cmd_group)
		return self._rbNumber

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .RbOffset import RbOffsetCls
			self._rbOffset = RbOffsetCls(self._core, self._cmd_group)
		return self._rbOffset

	@property
	def refactor(self):
		"""refactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_refactor'):
			from .Refactor import RefactorCls
			self._refactor = RefactorCls(self._core, self._cmd_group)
		return self._refactor

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetitions'):
			from .Repetitions import RepetitionsCls
			self._repetitions = RepetitionsCls(self._core, self._cmd_group)
		return self._repetitions

	@property
	def rimRs(self):
		"""rimRs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rimRs'):
			from .RimRs import RimRsCls
			self._rimRs = RimRsCls(self._core, self._cmd_group)
		return self._rimRs

	@property
	def row(self):
		"""row commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	@property
	def rsType(self):
		"""rsType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsType'):
			from .RsType import RsTypeCls
			self._rsType = RsTypeCls(self._core, self._cmd_group)
		return self._rsType

	@property
	def sci(self):
		"""sci commands group. 22 Sub-classes, 0 commands."""
		if not hasattr(self, '_sci'):
			from .Sci import SciCls
			self._sci = SciCls(self._core, self._cmd_group)
		return self._sci

	@property
	def scid(self):
		"""scid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scid'):
			from .Scid import ScidCls
			self._scid = ScidCls(self._core, self._cmd_group)
		return self._scid

	@property
	def seq(self):
		"""seq commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_seq'):
			from .Seq import SeqCls
			self._seq = SeqCls(self._core, self._cmd_group)
		return self._seq

	@property
	def seqLength(self):
		"""seqLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqLength'):
			from .SeqLength import SeqLengthCls
			self._seqLength = SeqLengthCls(self._core, self._cmd_group)
		return self._seqLength

	@property
	def sl(self):
		"""sl commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sl'):
			from .Sl import SlCls
			self._sl = SlCls(self._core, self._cmd_group)
		return self._sl

	@property
	def slot(self):
		"""slot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slot'):
			from .Slot import SlotCls
			self._slot = SlotCls(self._core, self._cmd_group)
		return self._slot

	@property
	def sltFmt(self):
		"""sltFmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sltFmt'):
			from .SltFmt import SltFmtCls
			self._sltFmt = SltFmtCls(self._core, self._cmd_group)
		return self._sltFmt

	@property
	def srIdx(self):
		"""srIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srIdx'):
			from .SrIdx import SrIdxCls
			self._srIdx = SrIdxCls(self._core, self._cmd_group)
		return self._srIdx

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def symNumber(self):
		"""symNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symNumber'):
			from .SymNumber import SymNumberCls
			self._symNumber = SymNumberCls(self._core, self._cmd_group)
		return self._symNumber

	@property
	def symOffset(self):
		"""symOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symOffset'):
			from .SymOffset import SymOffsetCls
			self._symOffset = SymOffsetCls(self._core, self._cmd_group)
		return self._symOffset

	@property
	def tbm(self):
		"""tbm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbm'):
			from .Tbm import TbmCls
			self._tbm = TbmCls(self._core, self._cmd_group)
		return self._tbm

	@property
	def tboms(self):
		"""tboms commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tboms'):
			from .Tboms import TbomsCls
			self._tboms = TbomsCls(self._core, self._cmd_group)
		return self._tboms

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Toffset import ToffsetCls
			self._toffset = ToffsetCls(self._core, self._cmd_group)
		return self._toffset

	@property
	def trtComb(self):
		"""trtComb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trtComb'):
			from .TrtComb import TrtCombCls
			self._trtComb = TrtCombCls(self._core, self._cmd_group)
		return self._trtComb

	@property
	def cw(self):
		"""cw commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_cw'):
			from .Cw import CwCls
			self._cw = CwCls(self._core, self._cmd_group)
		return self._cw

	def clone(self) -> 'AllocCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AllocCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
