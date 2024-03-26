from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VobsCls:
	"""Vobs commands group definition. 7 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vobs", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def morientation(self):
		"""morientation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_morientation'):
			from .Morientation import MorientationCls
			self._morientation = MorientationCls(self._core, self._cmd_group)
		return self._morientation

	@property
	def pmodel(self):
		"""pmodel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmodel'):
			from .Pmodel import PmodelCls
			self._pmodel = PmodelCls(self._core, self._cmd_group)
		return self._pmodel

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	@property
	def roffset(self):
		"""roffset commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_roffset'):
			from .Roffset import RoffsetCls
			self._roffset = RoffsetCls(self._core, self._cmd_group)
		return self._roffset

	def clone(self) -> 'VobsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = VobsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
