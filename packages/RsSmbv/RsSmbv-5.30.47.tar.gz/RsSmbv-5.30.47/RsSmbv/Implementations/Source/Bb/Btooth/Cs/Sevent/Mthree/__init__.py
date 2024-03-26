from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MthreeCls:
	"""Mthree commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mthree", core, parent)

	@property
	def nap(self):
		"""nap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nap'):
			from .Nap import NapCls
			self._nap = NapCls(self._core, self._cmd_group)
		return self._nap

	@property
	def tipt(self):
		"""tipt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tipt'):
			from .Tipt import TiptCls
			self._tipt = TiptCls(self._core, self._cmd_group)
		return self._tipt

	@property
	def tpm(self):
		"""tpm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpm'):
			from .Tpm import TpmCls
			self._tpm = TpmCls(self._core, self._cmd_group)
		return self._tpm

	@property
	def tsw(self):
		"""tsw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsw'):
			from .Tsw import TswCls
			self._tsw = TswCls(self._core, self._cmd_group)
		return self._tsw

	def clone(self) -> 'MthreeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MthreeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
