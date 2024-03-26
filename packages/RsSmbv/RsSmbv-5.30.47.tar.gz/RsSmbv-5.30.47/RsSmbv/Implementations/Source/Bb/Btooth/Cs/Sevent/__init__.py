from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeventCls:
	"""Sevent commands group definition. 34 total commands, 23 Subgroups, 0 group commands
	Repeated Capability: ChannelNull, default value after init: ChannelNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sevent", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channelNull_get', 'repcap_channelNull_set', repcap.ChannelNull.Nr0)

	def repcap_channelNull_set(self, channelNull: repcap.ChannelNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ChannelNull.Default
		Default value after init: ChannelNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(channelNull)

	def repcap_channelNull_get(self) -> repcap.ChannelNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .Dlist import DlistCls
			self._dlist = DlistCls(self._core, self._cmd_group)
		return self._dlist

	@property
	def mmaSteps(self):
		"""mmaSteps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmaSteps'):
			from .MmaSteps import MmaStepsCls
			self._mmaSteps = MmaStepsCls(self._core, self._cmd_group)
		return self._mmaSteps

	@property
	def mmiSteps(self):
		"""mmiSteps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmiSteps'):
			from .MmiSteps import MmiStepsCls
			self._mmiSteps = MmiStepsCls(self._core, self._cmd_group)
		return self._mmiSteps

	@property
	def mmode(self):
		"""mmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmode'):
			from .Mmode import MmodeCls
			self._mmode = MmodeCls(self._core, self._cmd_group)
		return self._mmode

	@property
	def mmRepetition(self):
		"""mmRepetition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmRepetition'):
			from .MmRepetition import MmRepetitionCls
			self._mmRepetition = MmRepetitionCls(self._core, self._cmd_group)
		return self._mmRepetition

	@property
	def mmSteps(self):
		"""mmSteps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmSteps'):
			from .MmSteps import MmStepsCls
			self._mmSteps = MmStepsCls(self._core, self._cmd_group)
		return self._mmSteps

	@property
	def mone(self):
		"""mone commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mone'):
			from .Mone import MoneCls
			self._mone = MoneCls(self._core, self._cmd_group)
		return self._mone

	@property
	def mthree(self):
		"""mthree commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_mthree'):
			from .Mthree import MthreeCls
			self._mthree = MthreeCls(self._core, self._cmd_group)
		return self._mthree

	@property
	def mtwo(self):
		"""mtwo commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_mtwo'):
			from .Mtwo import MtwoCls
			self._mtwo = MtwoCls(self._core, self._cmd_group)
		return self._mtwo

	@property
	def mzero(self):
		"""mzero commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mzero'):
			from .Mzero import MzeroCls
			self._mzero = MzeroCls(self._core, self._cmd_group)
		return self._mzero

	@property
	def mzSteps(self):
		"""mzSteps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mzSteps'):
			from .MzSteps import MzStepsCls
			self._mzSteps = MzStepsCls(self._core, self._cmd_group)
		return self._mzSteps

	@property
	def noStep(self):
		"""noStep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noStep'):
			from .NoStep import NoStepCls
			self._noStep = NoStepCls(self._core, self._cmd_group)
		return self._noStep

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def seqLength(self):
		"""seqLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqLength'):
			from .SeqLength import SeqLengthCls
			self._seqLength = SeqLengthCls(self._core, self._cmd_group)
		return self._seqLength

	@property
	def smode(self):
		"""smode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smode'):
			from .Smode import SmodeCls
			self._smode = SmodeCls(self._core, self._cmd_group)
		return self._smode

	@property
	def smStep(self):
		"""smStep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smStep'):
			from .SmStep import SmStepCls
			self._smStep = SmStepCls(self._core, self._cmd_group)
		return self._smStep

	@property
	def sspace(self):
		"""sspace commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sspace'):
			from .Sspace import SspaceCls
			self._sspace = SspaceCls(self._core, self._cmd_group)
		return self._sspace

	@property
	def stype(self):
		"""stype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stype'):
			from .Stype import StypeCls
			self._stype = StypeCls(self._core, self._cmd_group)
		return self._stype

	@property
	def tfcs(self):
		"""tfcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfcs'):
			from .Tfcs import TfcsCls
			self._tfcs = TfcsCls(self._core, self._cmd_group)
		return self._tfcs

	@property
	def upayload(self):
		"""upayload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_upayload'):
			from .Upayload import UpayloadCls
			self._upayload = UpayloadCls(self._core, self._cmd_group)
		return self._upayload

	@property
	def upPattern(self):
		"""upPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_upPattern'):
			from .UpPattern import UpPatternCls
			self._upPattern = UpPatternCls(self._core, self._cmd_group)
		return self._upPattern

	@property
	def step(self):
		"""step commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_step'):
			from .Step import StepCls
			self._step = StepCls(self._core, self._cmd_group)
		return self._step

	def clone(self) -> 'SeventCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SeventCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
