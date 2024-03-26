from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DchannelCls:
	"""Dchannel commands group definition. 21 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dchannel", core, parent)

	@property
	def clength(self):
		"""clength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_clength'):
			from .Clength import ClengthCls
			self._clength = ClengthCls(self._core, self._cmd_group)
		return self._clength

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def drate(self):
		"""drate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_drate'):
			from .Drate import DrateCls
			self._drate = DrateCls(self._core, self._cmd_group)
		return self._drate

	@property
	def fcs(self):
		"""fcs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcs'):
			from .Fcs import FcsCls
			self._fcs = FcsCls(self._core, self._cmd_group)
		return self._fcs

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def packet(self):
		"""packet commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_packet'):
			from .Packet import PacketCls
			self._packet = PacketCls(self._core, self._cmd_group)
		return self._packet

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'DchannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DchannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
