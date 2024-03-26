from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MimoCls:
	"""Mimo commands group definition. 11 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mimo", core, parent)

	@property
	def poaAck(self):
		"""poaAck commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poaAck'):
			from .PoaAck import PoaAckCls
			self._poaAck = PoaAckCls(self._core, self._cmd_group)
		return self._poaAck

	@property
	def poaNack(self):
		"""poaNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poaNack'):
			from .PoaNack import PoaNackCls
			self._poaNack = PoaNackCls(self._core, self._cmd_group)
		return self._poaNack

	@property
	def poca(self):
		"""poca commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poca'):
			from .Poca import PocaCls
			self._poca = PocaCls(self._core, self._cmd_group)
		return self._poca

	@property
	def poNack(self):
		"""poNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poNack'):
			from .PoNack import PoNackCls
			self._poNack = PoNackCls(self._core, self._cmd_group)
		return self._poNack

	@property
	def ponNack(self):
		"""ponNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ponNack'):
			from .PonNack import PonNackCls
			self._ponNack = PonNackCls(self._core, self._cmd_group)
		return self._ponNack

	@property
	def tti(self):
		"""tti commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tti'):
			from .Tti import TtiCls
			self._tti = TtiCls(self._core, self._cmd_group)
		return self._tti

	@property
	def ttiCount(self):
		"""ttiCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiCount'):
			from .TtiCount import TtiCountCls
			self._ttiCount = TtiCountCls(self._core, self._cmd_group)
		return self._ttiCount

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	def clone(self) -> 'MimoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MimoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
