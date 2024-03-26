from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ECls:
	"""E commands group definition. 41 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("e", core, parent)

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .Ccode import CcodeCls
			self._ccode = CcodeCls(self._core, self._cmd_group)
		return self._ccode

	@property
	def dtx(self):
		"""dtx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtx'):
			from .Dtx import DtxCls
			self._dtx = DtxCls(self._core, self._cmd_group)
		return self._dtx

	@property
	def frc(self):
		"""frc commands group. 17 Sub-classes, 0 commands."""
		if not hasattr(self, '_frc'):
			from .Frc import FrcCls
			self._frc = FrcCls(self._core, self._cmd_group)
		return self._frc

	@property
	def hbit(self):
		"""hbit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hbit'):
			from .Hbit import HbitCls
			self._hbit = HbitCls(self._core, self._cmd_group)
		return self._hbit

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def rsNumber(self):
		"""rsNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsNumber'):
			from .RsNumber import RsNumberCls
			self._rsNumber = RsNumberCls(self._core, self._cmd_group)
		return self._rsNumber

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tfci(self):
		"""tfci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfci'):
			from .Tfci import TfciCls
			self._tfci = TfciCls(self._core, self._cmd_group)
		return self._tfci

	def clone(self) -> 'ECls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ECls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
