from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhichCls:
	"""Phich commands group definition. 6 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phich", core, parent)

	@property
	def anPattern(self):
		"""anPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anPattern'):
			from .AnPattern import AnPatternCls
			self._anPattern = AnPatternCls(self._core, self._cmd_group)
		return self._anPattern

	@property
	def cell(self):
		"""cell commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	@property
	def pmode(self):
		"""pmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmode'):
			from .Pmode import PmodeCls
			self._pmode = PmodeCls(self._core, self._cmd_group)
		return self._pmode

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	def clone(self) -> 'PhichCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PhichCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
