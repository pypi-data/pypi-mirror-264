from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PdcchCls:
	"""Pdcch commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdcch", core, parent)

	@property
	def nmAdaption(self):
		"""nmAdaption commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nmAdaption'):
			from .NmAdaption import NmAdaptionCls
			self._nmAdaption = NmAdaptionCls(self._core, self._cmd_group)
		return self._nmAdaption

	@property
	def nt3C(self):
		"""nt3C commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nt3C'):
			from .Nt3C import Nt3CCls
			self._nt3C = Nt3CCls(self._core, self._cmd_group)
		return self._nt3C

	@property
	def numPreempt(self):
		"""numPreempt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_numPreempt'):
			from .NumPreempt import NumPreemptCls
			self._numPreempt = NumPreemptCls(self._core, self._cmd_group)
		return self._numPreempt

	def clone(self) -> 'PdcchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PdcchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
