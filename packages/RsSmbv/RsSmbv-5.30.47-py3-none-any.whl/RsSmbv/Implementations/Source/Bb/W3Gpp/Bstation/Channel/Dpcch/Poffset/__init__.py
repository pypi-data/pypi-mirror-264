from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PoffsetCls:
	"""Poffset commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("poffset", core, parent)

	@property
	def pilot(self):
		"""pilot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pilot'):
			from .Pilot import PilotCls
			self._pilot = PilotCls(self._core, self._cmd_group)
		return self._pilot

	@property
	def tfci(self):
		"""tfci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .Tfci import TfciCls
			self._tfci = TfciCls(self._core, self._cmd_group)
		return self._tfci

	@property
	def tpc(self):
		"""tpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpc'):
			from .Tpc import TpcCls
			self._tpc = TpcCls(self._core, self._cmd_group)
		return self._tpc

	def clone(self) -> 'PoffsetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PoffsetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
