from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PsduCls:
	"""Psdu commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("psdu", core, parent)

	@property
	def brate(self):
		"""brate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_brate'):
			from .Brate import BrateCls
			self._brate = BrateCls(self._core, self._cmd_group)
		return self._brate

	@property
	def bspreading(self):
		"""bspreading commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bspreading'):
			from .Bspreading import BspreadingCls
			self._bspreading = BspreadingCls(self._core, self._cmd_group)
		return self._bspreading

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	def clone(self) -> 'PsduCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PsduCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
