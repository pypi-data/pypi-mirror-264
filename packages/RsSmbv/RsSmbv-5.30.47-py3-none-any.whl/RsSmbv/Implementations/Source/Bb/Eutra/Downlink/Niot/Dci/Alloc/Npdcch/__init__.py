from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NpdcchCls:
	"""Npdcch commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("npdcch", core, parent)

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Fmt import FmtCls
			self._fmt = FmtCls(self._core, self._cmd_group)
		return self._fmt

	@property
	def oind(self):
		"""oind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oind'):
			from .Oind import OindCls
			self._oind = OindCls(self._core, self._cmd_group)
		return self._oind

	@property
	def rep(self):
		"""rep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rep'):
			from .Rep import RepCls
			self._rep = RepCls(self._core, self._cmd_group)
		return self._rep

	def clone(self) -> 'NpdcchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NpdcchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
