from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CblockCls:
	"""Cblock commands group definition. 129 total commands, 107 Subgroups, 2 group commands
	Repeated Capability: CommandBlock, default value after init: CommandBlock.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cblock", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_commandBlock_get', 'repcap_commandBlock_set', repcap.CommandBlock.Nr1)

	def repcap_commandBlock_set(self, commandBlock: repcap.CommandBlock) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CommandBlock.Default
		Default value after init: CommandBlock.Nr1"""
		self._cmd_group.set_repcap_enum_value(commandBlock)

	def repcap_commandBlock_get(self) -> repcap.CommandBlock:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def achk(self):
		"""achk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_achk'):
			from .Achk import AchkCls
			self._achk = AchkCls(self._core, self._cmd_group)
		return self._achk

	@property
	def adata(self):
		"""adata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adata'):
			from .Adata import AdataCls
			self._adata = AdataCls(self._core, self._cmd_group)
		return self._adata

	@property
	def adCoding(self):
		"""adCoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adCoding'):
			from .AdCoding import AdCodingCls
			self._adCoding = AdCodingCls(self._core, self._cmd_group)
		return self._adCoding

	@property
	def afi(self):
		"""afi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_afi'):
			from .Afi import AfiCls
			self._afi = AfiCls(self._core, self._cmd_group)
		return self._afi

	@property
	def aid(self):
		"""aid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aid'):
			from .Aid import AidCls
			self._aid = AidCls(self._core, self._cmd_group)
		return self._aid

	@property
	def alength(self):
		"""alength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alength'):
			from .Alength import AlengthCls
			self._alength = AlengthCls(self._core, self._cmd_group)
		return self._alength

	@property
	def anSelection(self):
		"""anSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anSelection'):
			from .AnSelection import AnSelectionCls
			self._anSelection = AnSelectionCls(self._core, self._cmd_group)
		return self._anSelection

	@property
	def apfSupported(self):
		"""apfSupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apfSupported'):
			from .ApfSupported import ApfSupportedCls
			self._apfSupported = ApfSupportedCls(self._core, self._cmd_group)
		return self._apfSupported

	@property
	def apGeneric(self):
		"""apGeneric commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_apGeneric'):
			from .ApGeneric import ApGenericCls
			self._apGeneric = ApGenericCls(self._core, self._cmd_group)
		return self._apGeneric

	@property
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Append import AppendCls
			self._append = AppendCls(self._core, self._cmd_group)
		return self._append

	@property
	def atimeout(self):
		"""atimeout commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atimeout'):
			from .Atimeout import AtimeoutCls
			self._atimeout = AtimeoutCls(self._core, self._cmd_group)
		return self._atimeout

	@property
	def aupdate(self):
		"""aupdate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aupdate'):
			from .Aupdate import AupdateCls
			self._aupdate = AupdateCls(self._core, self._cmd_group)
		return self._aupdate

	@property
	def bccError(self):
		"""bccError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bccError'):
			from .BccError import BccErrorCls
			self._bccError = BccErrorCls(self._core, self._cmd_group)
		return self._bccError

	@property
	def bchk(self):
		"""bchk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bchk'):
			from .Bchk import BchkCls
			self._bchk = BchkCls(self._core, self._cmd_group)
		return self._bchk

	@property
	def bfsdd(self):
		"""bfsdd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bfsdd'):
			from .Bfsdd import BfsddCls
			self._bfsdd = BfsddCls(self._core, self._cmd_group)
		return self._bfsdd

	@property
	def blkSelection(self):
		"""blkSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_blkSelection'):
			from .BlkSelection import BlkSelectionCls
			self._blkSelection = BlkSelectionCls(self._core, self._cmd_group)
		return self._blkSelection

	@property
	def block(self):
		"""block commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_block'):
			from .Block import BlockCls
			self._block = BlockCls(self._core, self._cmd_group)
		return self._block

	@property
	def bno(self):
		"""bno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bno'):
			from .Bno import BnoCls
			self._bno = BnoCls(self._core, self._cmd_group)
		return self._bno

	@property
	def bpGeneric(self):
		"""bpGeneric commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpGeneric'):
			from .BpGeneric import BpGenericCls
			self._bpGeneric = BpGenericCls(self._core, self._cmd_group)
		return self._bpGeneric

	@property
	def btype(self):
		"""btype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_btype'):
			from .Btype import BtypeCls
			self._btype = BtypeCls(self._core, self._cmd_group)
		return self._btype

	@property
	def bupdate(self):
		"""bupdate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bupdate'):
			from .Bupdate import BupdateCls
			self._bupdate = BupdateCls(self._core, self._cmd_group)
		return self._bupdate

	@property
	def bytSelection(self):
		"""bytSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bytSelection'):
			from .BytSelection import BytSelectionCls
			self._bytSelection = BytSelectionCls(self._core, self._cmd_group)
		return self._bytSelection

	@property
	def cfgType(self):
		"""cfgType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfgType'):
			from .CfgType import CfgTypeCls
			self._cfgType = CfgTypeCls(self._core, self._cmd_group)
		return self._cfgType

	@property
	def chaining(self):
		"""chaining commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chaining'):
			from .Chaining import ChainingCls
			self._chaining = ChainingCls(self._core, self._cmd_group)
		return self._chaining

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .Ctype import CtypeCls
			self._ctype = CtypeCls(self._core, self._cmd_group)
		return self._ctype

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def deqd(self):
		"""deqd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deqd'):
			from .Deqd import DeqdCls
			self._deqd = DeqdCls(self._core, self._cmd_group)
		return self._deqd

	@property
	def dfollowing(self):
		"""dfollowing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfollowing'):
			from .Dfollowing import DfollowingCls
			self._dfollowing = DfollowingCls(self._core, self._cmd_group)
		return self._dfollowing

	@property
	def did(self):
		"""did commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_did'):
			from .Did import DidCls
			self._did = DidCls(self._core, self._cmd_group)
		return self._did

	@property
	def dlp2(self):
		"""dlp2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlp2'):
			from .Dlp2 import Dlp2Cls
			self._dlp2 = Dlp2Cls(self._core, self._cmd_group)
		return self._dlp2

	@property
	def dlp4(self):
		"""dlp4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlp4'):
			from .Dlp4 import Dlp4Cls
			self._dlp4 = Dlp4Cls(self._core, self._cmd_group)
		return self._dlp4

	@property
	def dlp8(self):
		"""dlp8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlp8'):
			from .Dlp8 import Dlp8Cls
			self._dlp8 = Dlp8Cls(self._core, self._cmd_group)
		return self._dlp8

	@property
	def dltPoll(self):
		"""dltPoll commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dltPoll'):
			from .DltPoll import DltPollCls
			self._dltPoll = DltPollCls(self._core, self._cmd_group)
		return self._dltPoll

	@property
	def dpl2(self):
		"""dpl2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpl2'):
			from .Dpl2 import Dpl2Cls
			self._dpl2 = Dpl2Cls(self._core, self._cmd_group)
		return self._dpl2

	@property
	def dpl4(self):
		"""dpl4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpl4'):
			from .Dpl4 import Dpl4Cls
			self._dpl4 = Dpl4Cls(self._core, self._cmd_group)
		return self._dpl4

	@property
	def dpl8(self):
		"""dpl8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpl8'):
			from .Dpl8 import Dpl8Cls
			self._dpl8 = Dpl8Cls(self._core, self._cmd_group)
		return self._dpl8

	@property
	def dptListen(self):
		"""dptListen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dptListen'):
			from .DptListen import DptListenCls
			self._dptListen = DptListenCls(self._core, self._cmd_group)
		return self._dptListen

	@property
	def dri(self):
		"""dri commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dri'):
			from .Dri import DriCls
			self._dri = DriCls(self._core, self._cmd_group)
		return self._dri

	@property
	def dsi(self):
		"""dsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsi'):
			from .Dsi import DsiCls
			self._dsi = DsiCls(self._core, self._cmd_group)
		return self._dsi

	@property
	def dsupported(self):
		"""dsupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsupported'):
			from .Dsupported import DsupportedCls
			self._dsupported = DsupportedCls(self._core, self._cmd_group)
		return self._dsupported

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def dwSelection(self):
		"""dwSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dwSelection'):
			from .DwSelection import DwSelectionCls
			self._dwSelection = DwSelectionCls(self._core, self._cmd_group)
		return self._dwSelection

	@property
	def echk(self):
		"""echk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_echk'):
			from .Echk import EchkCls
			self._echk = EchkCls(self._core, self._cmd_group)
		return self._echk

	@property
	def esSupported(self):
		"""esSupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_esSupported'):
			from .EsSupported import EsSupportedCls
			self._esSupported = EsSupportedCls(self._core, self._cmd_group)
		return self._esSupported

	@property
	def eupd(self):
		"""eupd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eupd'):
			from .Eupd import EupdCls
			self._eupd = EupdCls(self._core, self._cmd_group)
		return self._eupd

	@property
	def fpGeneric(self):
		"""fpGeneric commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_fpGeneric'):
			from .FpGeneric import FpGenericCls
			self._fpGeneric = FpGenericCls(self._core, self._cmd_group)
		return self._fpGeneric

	@property
	def fsc(self):
		"""fsc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fsc'):
			from .Fsc import FscCls
			self._fsc = FscCls(self._core, self._cmd_group)
		return self._fsc

	@property
	def fwi(self):
		"""fwi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fwi'):
			from .Fwi import FwiCls
			self._fwi = FwiCls(self._core, self._cmd_group)
		return self._fwi

	@property
	def gbSelection(self):
		"""gbSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gbSelection'):
			from .GbSelection import GbSelectionCls
			self._gbSelection = GbSelectionCls(self._core, self._cmd_group)
		return self._gbSelection

	@property
	def gdAvailable(self):
		"""gdAvailable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gdAvailable'):
			from .GdAvailable import GdAvailableCls
			self._gdAvailable = GdAvailableCls(self._core, self._cmd_group)
		return self._gdAvailable

	@property
	def ibNumber(self):
		"""ibNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ibNumber'):
			from .IbNumber import IbNumberCls
			self._ibNumber = IbNumberCls(self._core, self._cmd_group)
		return self._ibNumber

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Insert import InsertCls
			self._insert = InsertCls(self._core, self._cmd_group)
		return self._insert

	@property
	def kparameter(self):
		"""kparameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kparameter'):
			from .Kparameter import KparameterCls
			self._kparameter = KparameterCls(self._core, self._cmd_group)
		return self._kparameter

	@property
	def lreduction(self):
		"""lreduction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lreduction'):
			from .Lreduction import LreductionCls
			self._lreduction = LreductionCls(self._core, self._cmd_group)
		return self._lreduction

	@property
	def mbli(self):
		"""mbli commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mbli'):
			from .Mbli import MbliCls
			self._mbli = MbliCls(self._core, self._cmd_group)
		return self._mbli

	@property
	def miChaining(self):
		"""miChaining commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_miChaining'):
			from .MiChaining import MiChainingCls
			self._miChaining = MiChainingCls(self._core, self._cmd_group)
		return self._miChaining

	@property
	def mtR0(self):
		"""mtR0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtR0'):
			from .MtR0 import MtR0Cls
			self._mtR0 = MtR0Cls(self._core, self._cmd_group)
		return self._mtR0

	@property
	def mtR1(self):
		"""mtR1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtR1'):
			from .MtR1 import MtR1Cls
			self._mtR1 = MtR1Cls(self._core, self._cmd_group)
		return self._mtR1

	@property
	def mtR2(self):
		"""mtR2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtR2'):
			from .MtR2 import MtR2Cls
			self._mtR2 = MtR2Cls(self._core, self._cmd_group)
		return self._mtR2

	@property
	def n2Ftype(self):
		"""n2Ftype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Ftype'):
			from .N2Ftype import N2FtypeCls
			self._n2Ftype = N2FtypeCls(self._core, self._cmd_group)
		return self._n2Ftype

	@property
	def nack(self):
		"""nack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nack'):
			from .Nack import NackCls
			self._nack = NackCls(self._core, self._cmd_group)
		return self._nack

	@property
	def nad(self):
		"""nad commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nad'):
			from .Nad import NadCls
			self._nad = NadCls(self._core, self._cmd_group)
		return self._nad

	@property
	def nblocks(self):
		"""nblocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nblocks'):
			from .Nblocks import NblocksCls
			self._nblocks = NblocksCls(self._core, self._cmd_group)
		return self._nblocks

	@property
	def nfollowing(self):
		"""nfollowing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nfollowing'):
			from .Nfollowing import NfollowingCls
			self._nfollowing = NfollowingCls(self._core, self._cmd_group)
		return self._nfollowing

	@property
	def nid0(self):
		"""nid0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nid0'):
			from .Nid0 import Nid0Cls
			self._nid0 = Nid0Cls(self._core, self._cmd_group)
		return self._nid0

	@property
	def nid1(self):
		"""nid1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nid1'):
			from .Nid1 import Nid1Cls
			self._nid1 = Nid1Cls(self._core, self._cmd_group)
		return self._nid1

	@property
	def nid2(self):
		"""nid2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nid2'):
			from .Nid2 import Nid2Cls
			self._nid2 = Nid2Cls(self._core, self._cmd_group)
		return self._nid2

	@property
	def nnComplete(self):
		"""nnComplete commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nnComplete'):
			from .NnComplete import NnCompleteCls
			self._nnComplete = NnCompleteCls(self._core, self._cmd_group)
		return self._nnComplete

	@property
	def noApplications(self):
		"""noApplications commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noApplications'):
			from .NoApplications import NoApplicationsCls
			self._noApplications = NoApplicationsCls(self._core, self._cmd_group)
		return self._noApplications

	@property
	def noSlots(self):
		"""noSlots commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noSlots'):
			from .NoSlots import NoSlotsCls
			self._noSlots = NoSlotsCls(self._core, self._cmd_group)
		return self._noSlots

	@property
	def nservices(self):
		"""nservices commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nservices'):
			from .Nservices import NservicesCls
			self._nservices = NservicesCls(self._core, self._cmd_group)
		return self._nservices

	@property
	def nsize(self):
		"""nsize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsize'):
			from .Nsize import NsizeCls
			self._nsize = NsizeCls(self._core, self._cmd_group)
		return self._nsize

	@property
	def nsupported(self):
		"""nsupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsupported'):
			from .Nsupported import NsupportedCls
			self._nsupported = NsupportedCls(self._core, self._cmd_group)
		return self._nsupported

	@property
	def pad0(self):
		"""pad0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pad0'):
			from .Pad0 import Pad0Cls
			self._pad0 = Pad0Cls(self._core, self._cmd_group)
		return self._pad0

	@property
	def pad1(self):
		"""pad1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pad1'):
			from .Pad1 import Pad1Cls
			self._pad1 = Pad1Cls(self._core, self._cmd_group)
		return self._pad1

	@property
	def pad2(self):
		"""pad2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pad2'):
			from .Pad2 import Pad2Cls
			self._pad2 = Pad2Cls(self._core, self._cmd_group)
		return self._pad2

	@property
	def paste(self):
		"""paste commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paste'):
			from .Paste import PasteCls
			self._paste = PasteCls(self._core, self._cmd_group)
		return self._paste

	@property
	def pduType(self):
		"""pduType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pduType'):
			from .PduType import PduTypeCls
			self._pduType = PduTypeCls(self._core, self._cmd_group)
		return self._pduType

	@property
	def plin(self):
		"""plin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plin'):
			from .Plin import PlinCls
			self._plin = PlinCls(self._core, self._cmd_group)
		return self._plin

	@property
	def plir(self):
		"""plir commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plir'):
			from .Plir import PlirCls
			self._plir = PlirCls(self._core, self._cmd_group)
		return self._plir

	@property
	def pni(self):
		"""pni commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pni'):
			from .Pni import PniCls
			self._pni = PniCls(self._core, self._cmd_group)
		return self._pni

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Poffset import PoffsetCls
			self._poffset = PoffsetCls(self._core, self._cmd_group)
		return self._poffset

	@property
	def pselection(self):
		"""pselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pselection'):
			from .Pselection import PselectionCls
			self._pselection = PselectionCls(self._core, self._cmd_group)
		return self._pselection

	@property
	def rc(self):
		"""rc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rc'):
			from .Rc import RcCls
			self._rc = RcCls(self._core, self._cmd_group)
		return self._rc

	@property
	def repetition(self):
		"""repetition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetition'):
			from .Repetition import RepetitionCls
			self._repetition = RepetitionCls(self._core, self._cmd_group)
		return self._repetition

	@property
	def rtox(self):
		"""rtox commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rtox'):
			from .Rtox import RtoxCls
			self._rtox = RtoxCls(self._core, self._cmd_group)
		return self._rtox

	@property
	def samples(self):
		"""samples commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_samples'):
			from .Samples import SamplesCls
			self._samples = SamplesCls(self._core, self._cmd_group)
		return self._samples

	@property
	def scmd(self):
		"""scmd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scmd'):
			from .Scmd import ScmdCls
			self._scmd = ScmdCls(self._core, self._cmd_group)
		return self._scmd

	@property
	def scode(self):
		"""scode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Scode import ScodeCls
			self._scode = ScodeCls(self._core, self._cmd_group)
		return self._scode

	@property
	def segSelection(self):
		"""segSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_segSelection'):
			from .SegSelection import SegSelectionCls
			self._segSelection = SegSelectionCls(self._core, self._cmd_group)
		return self._segSelection

	@property
	def senRequired(self):
		"""senRequired commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_senRequired'):
			from .SenRequired import SenRequiredCls
			self._senRequired = SenRequiredCls(self._core, self._cmd_group)
		return self._senRequired

	@property
	def service(self):
		"""service commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_service'):
			from .Service import ServiceCls
			self._service = ServiceCls(self._core, self._cmd_group)
		return self._service

	@property
	def sf1(self):
		"""sf1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf1'):
			from .Sf1 import Sf1Cls
			self._sf1 = Sf1Cls(self._core, self._cmd_group)
		return self._sf1

	@property
	def sf2(self):
		"""sf2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf2'):
			from .Sf2 import Sf2Cls
			self._sf2 = Sf2Cls(self._core, self._cmd_group)
		return self._sf2

	@property
	def sfgi(self):
		"""sfgi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfgi'):
			from .Sfgi import SfgiCls
			self._sfgi = SfgiCls(self._core, self._cmd_group)
		return self._sfgi

	@property
	def sno(self):
		"""sno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sno'):
			from .Sno import SnoCls
			self._sno = SnoCls(self._core, self._cmd_group)
		return self._sno

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .Snumber import SnumberCls
			self._snumber = SnumberCls(self._core, self._cmd_group)
		return self._snumber

	@property
	def spLower(self):
		"""spLower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spLower'):
			from .SpLower import SpLowerCls
			self._spLower = SpLowerCls(self._core, self._cmd_group)
		return self._spLower

	@property
	def spUpper(self):
		"""spUpper commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spUpper'):
			from .SpUpper import SpUpperCls
			self._spUpper = SpUpperCls(self._core, self._cmd_group)
		return self._spUpper

	@property
	def ssnRequired(self):
		"""ssnRequired commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssnRequired'):
			from .SsnRequired import SsnRequiredCls
			self._ssnRequired = SsnRequiredCls(self._core, self._cmd_group)
		return self._ssnRequired

	@property
	def stime(self):
		"""stime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stime'):
			from .Stime import StimeCls
			self._stime = StimeCls(self._core, self._cmd_group)
		return self._stime

	@property
	def t1Tconfigured(self):
		"""t1Tconfigured commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t1Tconfigured'):
			from .T1Tconfigured import T1TconfiguredCls
			self._t1Tconfigured = T1TconfiguredCls(self._core, self._cmd_group)
		return self._t1Tconfigured

	@property
	def t1Tk(self):
		"""t1Tk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t1Tk'):
			from .T1Tk import T1TkCls
			self._t1Tk = T1TkCls(self._core, self._cmd_group)
		return self._t1Tk

	@property
	def taipicc(self):
		"""taipicc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taipicc'):
			from .Taipicc import TaipiccCls
			self._taipicc = TaipiccCls(self._core, self._cmd_group)
		return self._taipicc

	@property
	def tsn(self):
		"""tsn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsn'):
			from .Tsn import TsnCls
			self._tsn = TsnCls(self._core, self._cmd_group)
		return self._tsn

	@property
	def wt(self):
		"""wt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wt'):
			from .Wt import WtCls
			self._wt = WtCls(self._core, self._cmd_group)
		return self._wt

	@property
	def wtxm(self):
		"""wtxm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wtxm'):
			from .Wtxm import WtxmCls
			self._wtxm = WtxmCls(self._core, self._cmd_group)
		return self._wtxm

	def copy(self, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:COPY \n
		Snippet: driver.source.bb.nfc.cblock.copy(commandBlock = repcap.CommandBlock.Default) \n
		Copies a command block for later use. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:COPY')

	def copy_with_opc(self, commandBlock=repcap.CommandBlock.Default, opc_timeout_ms: int = -1) -> None:
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:COPY \n
		Snippet: driver.source.bb.nfc.cblock.copy_with_opc(commandBlock = repcap.CommandBlock.Default) \n
		Copies a command block for later use. \n
		Same as copy, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:COPY', opc_timeout_ms)

	def delete(self, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DELete \n
		Snippet: driver.source.bb.nfc.cblock.delete(commandBlock = repcap.CommandBlock.Default) \n
		Removes a command block from the command sequence. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
		"""
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:DELete')

	def delete_with_opc(self, commandBlock=repcap.CommandBlock.Default, opc_timeout_ms: int = -1) -> None:
		commandBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DELete \n
		Snippet: driver.source.bb.nfc.cblock.delete_with_opc(commandBlock = repcap.CommandBlock.Default) \n
		Removes a command block from the command sequence. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:DELete', opc_timeout_ms)

	def clone(self) -> 'CblockCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CblockCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
