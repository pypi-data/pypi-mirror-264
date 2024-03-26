from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpdchCls:
	"""Dpdch commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpdch", core, parent)

	@property
	def fcio(self):
		"""fcio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fcio'):
			from .Fcio import FcioCls
			self._fcio = FcioCls(self._core, self._cmd_group)
		return self._fcio

	@property
	def orate(self):
		"""orate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_orate'):
			from .Orate import OrateCls
			self._orate = OrateCls(self._core, self._cmd_group)
		return self._orate

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'DpdchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpdchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
