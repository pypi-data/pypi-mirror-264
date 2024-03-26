from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BpGenericCls:
	"""BpGeneric commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bpGeneric", core, parent)

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dlength(self):
		"""dlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlength'):
			from .Dlength import DlengthCls
			self._dlength = DlengthCls(self._core, self._cmd_group)
		return self._dlength

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plength'):
			from .Plength import PlengthCls
			self._plength = PlengthCls(self._core, self._cmd_group)
		return self._plength

	def clone(self) -> 'BpGenericCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BpGenericCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
