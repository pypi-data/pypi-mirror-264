from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DchCls:
	"""Dch commands group definition. 88 total commands, 17 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dch", core, parent)

	@property
	def bit(self):
		"""bit commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bit'):
			from .Bit import BitCls
			self._bit = BitCls(self._core, self._cmd_group)
		return self._bit

	@property
	def block(self):
		"""block commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_block'):
			from .Block import BlockCls
			self._block = BlockCls(self._core, self._cmd_group)
		return self._block

	@property
	def bpFrame(self):
		"""bpFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpFrame'):
			from .BpFrame import BpFrameCls
			self._bpFrame = BpFrameCls(self._core, self._cmd_group)
		return self._bpFrame

	@property
	def ccount(self):
		"""ccount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccount'):
			from .Ccount import CcountCls
			self._ccount = CcountCls(self._core, self._cmd_group)
		return self._ccount

	@property
	def dcch(self):
		"""dcch commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcch'):
			from .Dcch import DcchCls
			self._dcch = DcchCls(self._core, self._cmd_group)
		return self._dcch

	@property
	def dtch(self):
		"""dtch commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtch'):
			from .Dtch import DtchCls
			self._dtch = DtchCls(self._core, self._cmd_group)
		return self._dtch

	@property
	def hsch(self):
		"""hsch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsch'):
			from .Hsch import HschCls
			self._hsch = HschCls(self._core, self._cmd_group)
		return self._hsch

	@property
	def hsdpa(self):
		"""hsdpa commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsdpa'):
			from .Hsdpa import HsdpaCls
			self._hsdpa = HsdpaCls(self._core, self._cmd_group)
		return self._hsdpa

	@property
	def hsich(self):
		"""hsich commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsich'):
			from .Hsich import HsichCls
			self._hsich = HsichCls(self._core, self._cmd_group)
		return self._hsich

	@property
	def hsupa(self):
		"""hsupa commands group. 20 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsupa'):
			from .Hsupa import HsupaCls
			self._hsupa = HsupaCls(self._core, self._cmd_group)
		return self._hsupa

	@property
	def rupLayer(self):
		"""rupLayer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rupLayer'):
			from .RupLayer import RupLayerCls
			self._rupLayer = RupLayerCls(self._core, self._cmd_group)
		return self._rupLayer

	@property
	def scsMode(self):
		"""scsMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scsMode'):
			from .ScsMode import ScsModeCls
			self._scsMode = ScsModeCls(self._core, self._cmd_group)
		return self._scsMode

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def slotState(self):
		"""slotState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slotState'):
			from .SlotState import SlotStateCls
			self._slotState = SlotStateCls(self._core, self._cmd_group)
		return self._slotState

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tsCount(self):
		"""tsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsCount'):
			from .TsCount import TsCountCls
			self._tsCount = TsCountCls(self._core, self._cmd_group)
		return self._tsCount

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'DchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
