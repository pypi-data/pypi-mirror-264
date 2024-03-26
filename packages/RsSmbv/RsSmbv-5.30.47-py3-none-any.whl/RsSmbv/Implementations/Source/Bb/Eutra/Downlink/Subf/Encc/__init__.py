from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnccCls:
	"""Encc commands group definition. 96 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("encc", core, parent)

	@property
	def pcfich(self):
		"""pcfich commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcfich'):
			from .Pcfich import PcfichCls
			self._pcfich = PcfichCls(self._core, self._cmd_group)
		return self._pcfich

	@property
	def pdcch(self):
		"""pdcch commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdcch'):
			from .Pdcch import PdcchCls
			self._pdcch = PdcchCls(self._core, self._cmd_group)
		return self._pdcch

	@property
	def phich(self):
		"""phich commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_phich'):
			from .Phich import PhichCls
			self._phich = PhichCls(self._core, self._cmd_group)
		return self._phich

	@property
	def precoding(self):
		"""precoding commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_precoding'):
			from .Precoding import PrecodingCls
			self._precoding = PrecodingCls(self._core, self._cmd_group)
		return self._precoding

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Scrambling import ScramblingCls
			self._scrambling = ScramblingCls(self._core, self._cmd_group)
		return self._scrambling

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'EnccCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EnccCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
