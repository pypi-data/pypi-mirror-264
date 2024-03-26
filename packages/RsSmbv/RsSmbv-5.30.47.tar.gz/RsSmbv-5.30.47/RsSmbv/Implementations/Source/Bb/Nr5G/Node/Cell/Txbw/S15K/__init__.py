from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class S15KCls:
	"""S15K commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("s15K", core, parent)

	@property
	def komu(self):
		"""komu commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_komu'):
			from .Komu import KomuCls
			self._komu = KomuCls(self._core, self._cmd_group)
		return self._komu

	@property
	def nrb(self):
		"""nrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrb'):
			from .Nrb import NrbCls
			self._nrb = NrbCls(self._core, self._cmd_group)
		return self._nrb

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def use(self):
		"""use commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_use'):
			from .Use import UseCls
			self._use = UseCls(self._core, self._cmd_group)
		return self._use

	def clone(self) -> 'S15KCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = S15KCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
