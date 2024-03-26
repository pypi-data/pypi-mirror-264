from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimingCls:
	"""Timing commands group definition. 6 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("timing", core, parent)

	@property
	def dpower(self):
		"""dpower commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpower'):
			from .Dpower import DpowerCls
			self._dpower = DpowerCls(self._core, self._cmd_group)
		return self._dpower

	@property
	def soffset(self):
		"""soffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soffset'):
			from .Soffset import SoffsetCls
			self._soffset = SoffsetCls(self._core, self._cmd_group)
		return self._soffset

	@property
	def speriod(self):
		"""speriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_speriod'):
			from .Speriod import SperiodCls
			self._speriod = SperiodCls(self._core, self._cmd_group)
		return self._speriod

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	def clone(self) -> 'TimingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
