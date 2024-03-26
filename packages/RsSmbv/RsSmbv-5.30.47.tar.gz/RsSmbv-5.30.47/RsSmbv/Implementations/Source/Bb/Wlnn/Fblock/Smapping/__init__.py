from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SmappingCls:
	"""Smapping commands group definition. 6 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("smapping", core, parent)

	@property
	def bselection(self):
		"""bselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bselection'):
			from .Bselection import BselectionCls
			self._bselection = BselectionCls(self._core, self._cmd_group)
		return self._bselection

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Index import IndexCls
			self._index = IndexCls(self._core, self._cmd_group)
		return self._index

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def row(self):
		"""row commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	@property
	def tshift(self):
		"""tshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tshift'):
			from .Tshift import TshiftCls
			self._tshift = TshiftCls(self._core, self._cmd_group)
		return self._tshift

	def clone(self) -> 'SmappingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SmappingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
