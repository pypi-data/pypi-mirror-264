from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwpCls:
	"""Bwp commands group definition. 179 total commands, 21 Subgroups, 0 group commands
	Repeated Capability: BwPartNull, default value after init: BwPartNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bwp", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_bwPartNull_get', 'repcap_bwPartNull_set', repcap.BwPartNull.Nr0)

	def repcap_bwPartNull_set(self, bwPartNull: repcap.BwPartNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BwPartNull.Default
		Default value after init: BwPartNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(bwPartNull)

	def repcap_bwPartNull_get(self) -> repcap.BwPartNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def ciLength(self):
		"""ciLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ciLength'):
			from .CiLength import CiLengthCls
			self._ciLength = CiLengthCls(self._core, self._cmd_group)
		return self._ciLength

	@property
	def csi(self):
		"""csi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_csi'):
			from .Csi import CsiCls
			self._csi = CsiCls(self._core, self._cmd_group)
		return self._csi

	@property
	def csirs(self):
		"""csirs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_csirs'):
			from .Csirs import CsirsCls
			self._csirs = CsirsCls(self._core, self._cmd_group)
		return self._csirs

	@property
	def dci(self):
		"""dci commands group. 17 Sub-classes, 0 commands."""
		if not hasattr(self, '_dci'):
			from .Dci import DciCls
			self._dci = DciCls(self._core, self._cmd_group)
		return self._dci

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Dfreq import DfreqCls
			self._dfreq = DfreqCls(self._core, self._cmd_group)
		return self._dfreq

	@property
	def indicator(self):
		"""indicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indicator'):
			from .Indicator import IndicatorCls
			self._indicator = IndicatorCls(self._core, self._cmd_group)
		return self._indicator

	@property
	def naInd(self):
		"""naInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naInd'):
			from .NaInd import NaIndCls
			self._naInd = NaIndCls(self._core, self._cmd_group)
		return self._naInd

	@property
	def ncind(self):
		"""ncind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncind'):
			from .Ncind import NcindCls
			self._ncind = NcindCls(self._core, self._cmd_group)
		return self._ncind

	@property
	def pdcch(self):
		"""pdcch commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdcch'):
			from .Pdcch import PdcchCls
			self._pdcch = PdcchCls(self._core, self._cmd_group)
		return self._pdcch

	@property
	def pdsch(self):
		"""pdsch commands group. 28 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsch'):
			from .Pdsch import PdschCls
			self._pdsch = PdschCls(self._core, self._cmd_group)
		return self._pdsch

	@property
	def prbOffset(self):
		"""prbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbOffset'):
			from .PrbOffset import PrbOffsetCls
			self._prbOffset = PrbOffsetCls(self._core, self._cmd_group)
		return self._prbOffset

	@property
	def pucch(self):
		"""pucch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pucch'):
			from .Pucch import PucchCls
			self._pucch = PucchCls(self._core, self._cmd_group)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	@property
	def ratm(self):
		"""ratm commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ratm'):
			from .Ratm import RatmCls
			self._ratm = RatmCls(self._core, self._cmd_group)
		return self._ratm

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
	def rmc(self):
		"""rmc commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_rmc'):
			from .Rmc import RmcCls
			self._rmc = RmcCls(self._core, self._cmd_group)
		return self._rmc

	@property
	def rnti(self):
		"""rnti commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_rnti'):
			from .Rnti import RntiCls
			self._rnti = RntiCls(self._core, self._cmd_group)
		return self._rnti

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .ScSpacing import ScSpacingCls
			self._scSpacing = ScSpacingCls(self._core, self._cmd_group)
		return self._scSpacing

	@property
	def selFormat(self):
		"""selFormat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_selFormat'):
			from .SelFormat import SelFormatCls
			self._selFormat = SelFormatCls(self._core, self._cmd_group)
		return self._selFormat

	@property
	def srs(self):
		"""srs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_srs'):
			from .Srs import SrsCls
			self._srs = SrsCls(self._core, self._cmd_group)
		return self._srs

	def clone(self) -> 'BwpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BwpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
