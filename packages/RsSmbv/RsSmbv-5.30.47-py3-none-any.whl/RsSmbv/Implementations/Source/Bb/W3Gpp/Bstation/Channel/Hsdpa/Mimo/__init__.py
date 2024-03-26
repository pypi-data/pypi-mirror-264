from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MimoCls:
	"""Mimo commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mimo", core, parent)

	@property
	def cvpb(self):
		"""cvpb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cvpb'):
			from .Cvpb import CvpbCls
			self._cvpb = CvpbCls(self._core, self._cmd_group)
		return self._cvpb

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def pwPattern(self):
		"""pwPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pwPattern'):
			from .PwPattern import PwPatternCls
			self._pwPattern = PwPatternCls(self._core, self._cmd_group)
		return self._pwPattern

	@property
	def staPattern(self):
		"""staPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_staPattern'):
			from .StaPattern import StaPatternCls
			self._staPattern = StaPatternCls(self._core, self._cmd_group)
		return self._staPattern

	def clone(self) -> 'MimoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MimoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
