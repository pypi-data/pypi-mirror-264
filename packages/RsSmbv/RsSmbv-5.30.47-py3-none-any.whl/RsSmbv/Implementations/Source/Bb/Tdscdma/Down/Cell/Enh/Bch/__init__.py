from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BchCls:
	"""Bch commands group definition. 18 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bch", core, parent)

	@property
	def bpFrame(self):
		"""bpFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpFrame'):
			from .BpFrame import BpFrameCls
			self._bpFrame = BpFrameCls(self._core, self._cmd_group)
		return self._bpFrame

	@property
	def dtch(self):
		"""dtch commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtch'):
			from .Dtch import DtchCls
			self._dtch = DtchCls(self._core, self._cmd_group)
		return self._dtch

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
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'BchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
