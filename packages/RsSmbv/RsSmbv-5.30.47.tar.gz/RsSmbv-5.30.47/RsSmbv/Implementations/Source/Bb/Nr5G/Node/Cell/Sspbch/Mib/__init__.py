from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MibCls:
	"""Mib commands group definition. 10 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mib", core, parent)

	@property
	def asof(self):
		"""asof commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_asof'):
			from .Asof import AsofCls
			self._asof = AsofCls(self._core, self._cmd_group)
		return self._asof

	@property
	def cbarred(self):
		"""cbarred commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbarred'):
			from .Cbarred import CbarredCls
			self._cbarred = CbarredCls(self._core, self._cmd_group)
		return self._cbarred

	@property
	def csZero(self):
		"""csZero commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csZero'):
			from .CsZero import CsZeroCls
			self._csZero = CsZeroCls(self._core, self._cmd_group)
		return self._csZero

	@property
	def ifrResel(self):
		"""ifrResel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ifrResel'):
			from .IfrResel import IfrReselCls
			self._ifrResel = IfrReselCls(self._core, self._cmd_group)
		return self._ifrResel

	@property
	def scOffset(self):
		"""scOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scOffset'):
			from .ScOffset import ScOffsetCls
			self._scOffset = ScOffsetCls(self._core, self._cmd_group)
		return self._scOffset

	@property
	def scsc(self):
		"""scsc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scsc'):
			from .Scsc import ScscCls
			self._scsc = ScscCls(self._core, self._cmd_group)
		return self._scsc

	@property
	def sfOffset(self):
		"""sfOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfOffset'):
			from .SfOffset import SfOffsetCls
			self._sfOffset = SfOffsetCls(self._core, self._cmd_group)
		return self._sfOffset

	@property
	def spare(self):
		"""spare commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spare'):
			from .Spare import SpareCls
			self._spare = SpareCls(self._core, self._cmd_group)
		return self._spare

	@property
	def ssZero(self):
		"""ssZero commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssZero'):
			from .SsZero import SsZeroCls
			self._ssZero = SsZeroCls(self._core, self._cmd_group)
		return self._ssZero

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'MibCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MibCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
