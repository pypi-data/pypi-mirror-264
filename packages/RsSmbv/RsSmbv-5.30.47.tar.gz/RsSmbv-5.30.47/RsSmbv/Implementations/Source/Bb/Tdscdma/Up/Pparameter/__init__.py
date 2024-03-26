from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PparameterCls:
	"""Pparameter commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pparameter", core, parent)

	@property
	def dpch(self):
		"""dpch commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_dpch'):
			from .Dpch import DpchCls
			self._dpch = DpchCls(self._core, self._cmd_group)
		return self._dpch

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	def clone(self) -> 'PparameterCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PparameterCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
