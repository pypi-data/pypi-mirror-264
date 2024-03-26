from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SciCls:
	"""Sci commands group definition. 19 total commands, 19 Subgroups, 0 group commands
	Repeated Capability: IndexNull, default value after init: IndexNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sci", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_indexNull_get', 'repcap_indexNull_set', repcap.IndexNull.Nr0)

	def repcap_indexNull_set(self, indexNull: repcap.IndexNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IndexNull.Default
		Default value after init: IndexNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(indexNull)

	def repcap_indexNull_get(self) -> repcap.IndexNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def bitData(self):
		"""bitData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitData'):
			from .BitData import BitDataCls
			self._bitData = BitDataCls(self._core, self._cmd_group)
		return self._bitData

	@property
	def fhFlag(self):
		"""fhFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fhFlag'):
			from .FhFlag import FhFlagCls
			self._fhFlag = FhFlagCls(self._core, self._cmd_group)
		return self._fhFlag

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def freqResloc(self):
		"""freqResloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_freqResloc'):
			from .FreqResloc import FreqReslocCls
			self._freqResloc = FreqReslocCls(self._core, self._cmd_group)
		return self._freqResloc

	@property
	def grid(self):
		"""grid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_grid'):
			from .Grid import GridCls
			self._grid = GridCls(self._core, self._cmd_group)
		return self._grid

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Mcs import McsCls
			self._mcs = McsCls(self._core, self._cmd_group)
		return self._mcs

	@property
	def npscch(self):
		"""npscch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npscch'):
			from .Npscch import NpscchCls
			self._npscch = NpscchCls(self._core, self._cmd_group)
		return self._npscch

	@property
	def pririty(self):
		"""pririty commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pririty'):
			from .Pririty import PrirityCls
			self._pririty = PrirityCls(self._core, self._cmd_group)
		return self._pririty

	@property
	def pscPeriod(self):
		"""pscPeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pscPeriod'):
			from .PscPeriod import PscPeriodCls
			self._pscPeriod = PscPeriodCls(self._core, self._cmd_group)
		return self._pscPeriod

	@property
	def rbahoppAlloc(self):
		"""rbahoppAlloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbahoppAlloc'):
			from .RbahoppAlloc import RbahoppAllocCls
			self._rbahoppAlloc = RbahoppAllocCls(self._core, self._cmd_group)
		return self._rbahoppAlloc

	@property
	def rreservation(self):
		"""rreservation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rreservation'):
			from .Rreservation import RreservationCls
			self._rreservation = RreservationCls(self._core, self._cmd_group)
		return self._rreservation

	@property
	def sf(self):
		"""sf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf'):
			from .Sf import SfCls
			self._sf = SfCls(self._core, self._cmd_group)
		return self._sf

	@property
	def startSf(self):
		"""startSf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_startSf'):
			from .StartSf import StartSfCls
			self._startSf = StartSfCls(self._core, self._cmd_group)
		return self._startSf

	@property
	def subChannel(self):
		"""subChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subChannel'):
			from .SubChannel import SubChannelCls
			self._subChannel = SubChannelCls(self._core, self._cmd_group)
		return self._subChannel

	@property
	def taInd(self):
		"""taInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taInd'):
			from .TaInd import TaIndCls
			self._taInd = TaIndCls(self._core, self._cmd_group)
		return self._taInd

	@property
	def timGap(self):
		"""timGap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_timGap'):
			from .TimGap import TimGapCls
			self._timGap = TimGapCls(self._core, self._cmd_group)
		return self._timGap

	@property
	def trp(self):
		"""trp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trp'):
			from .Trp import TrpCls
			self._trp = TrpCls(self._core, self._cmd_group)
		return self._trp

	@property
	def txIndex(self):
		"""txIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txIndex'):
			from .TxIndex import TxIndexCls
			self._txIndex = TxIndexCls(self._core, self._cmd_group)
		return self._txIndex

	@property
	def txMode(self):
		"""txMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txMode'):
			from .TxMode import TxModeCls
			self._txMode = TxModeCls(self._core, self._cmd_group)
		return self._txMode

	def clone(self) -> 'SciCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SciCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
