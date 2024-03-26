from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpcchCls:
	"""Dpcch commands group definition. 13 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpcch", core, parent)

	@property
	def eucc(self):
		"""eucc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_eucc'):
			from .Eucc import EuccCls
			self._eucc = EuccCls(self._core, self._cmd_group)
		return self._eucc

	@property
	def sync(self):
		"""sync commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Sync import SyncCls
			self._sync = SyncCls(self._core, self._cmd_group)
		return self._sync

	@property
	def tfci(self):
		"""tfci commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tfci'):
			from .Tfci import TfciCls
			self._tfci = TfciCls(self._core, self._cmd_group)
		return self._tfci

	@property
	def tpc(self):
		"""tpc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Tpc import TpcCls
			self._tpc = TpcCls(self._core, self._cmd_group)
		return self._tpc

	def clone(self) -> 'DpcchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpcchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
