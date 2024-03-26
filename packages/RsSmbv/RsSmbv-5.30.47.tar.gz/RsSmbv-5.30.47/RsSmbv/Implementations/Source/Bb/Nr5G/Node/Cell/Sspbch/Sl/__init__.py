from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlCls:
	"""Sl commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sl", core, parent)

	@property
	def binPeriod(self):
		"""binPeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_binPeriod'):
			from .BinPeriod import BinPeriodCls
			self._binPeriod = BinPeriodCls(self._core, self._cmd_group)
		return self._binPeriod

	@property
	def inCoverage(self):
		"""inCoverage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inCoverage'):
			from .InCoverage import InCoverageCls
			self._inCoverage = InCoverageCls(self._core, self._cmd_group)
		return self._inCoverage

	@property
	def interval(self):
		"""interval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interval'):
			from .Interval import IntervalCls
			self._interval = IntervalCls(self._core, self._cmd_group)
		return self._interval

	@property
	def sbits(self):
		"""sbits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sbits'):
			from .Sbits import SbitsCls
			self._sbits = SbitsCls(self._core, self._cmd_group)
		return self._sbits

	@property
	def tddConf(self):
		"""tddConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tddConf'):
			from .TddConf import TddConfCls
			self._tddConf = TddConfCls(self._core, self._cmd_group)
		return self._tddConf

	@property
	def toffs(self):
		"""toffs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffs'):
			from .Toffs import ToffsCls
			self._toffs = ToffsCls(self._core, self._cmd_group)
		return self._toffs

	def clone(self) -> 'SlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
