from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyncCls:
	"""Sync commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sync", core, parent)

	@property
	def inCoverage(self):
		"""inCoverage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inCoverage'):
			from .InCoverage import InCoverageCls
			self._inCoverage = InCoverageCls(self._core, self._cmd_group)
		return self._inCoverage

	@property
	def offsetInd(self):
		"""offsetInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offsetInd'):
			from .OffsetInd import OffsetIndCls
			self._offsetInd = OffsetIndCls(self._core, self._cmd_group)
		return self._offsetInd

	@property
	def slssId(self):
		"""slssId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slssId'):
			from .SlssId import SlssIdCls
			self._slssId = SlssIdCls(self._core, self._cmd_group)
		return self._slssId

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'SyncCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SyncCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
