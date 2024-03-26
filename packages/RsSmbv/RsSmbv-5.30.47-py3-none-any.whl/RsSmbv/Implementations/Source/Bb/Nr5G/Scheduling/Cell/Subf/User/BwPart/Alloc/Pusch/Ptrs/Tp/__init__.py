from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpCls:
	"""Tp commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tp", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def ngrps(self):
		"""ngrps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ngrps'):
			from .Ngrps import NgrpsCls
			self._ngrps = NgrpsCls(self._core, self._cmd_group)
		return self._ngrps

	@property
	def scid(self):
		"""scid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scid'):
			from .Scid import ScidCls
			self._scid = ScidCls(self._core, self._cmd_group)
		return self._scid

	@property
	def sppg(self):
		"""sppg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sppg'):
			from .Sppg import SppgCls
			self._sppg = SppgCls(self._core, self._cmd_group)
		return self._sppg

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tmDensity(self):
		"""tmDensity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmDensity'):
			from .TmDensity import TmDensityCls
			self._tmDensity = TmDensityCls(self._core, self._cmd_group)
		return self._tmDensity

	def clone(self) -> 'TpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
