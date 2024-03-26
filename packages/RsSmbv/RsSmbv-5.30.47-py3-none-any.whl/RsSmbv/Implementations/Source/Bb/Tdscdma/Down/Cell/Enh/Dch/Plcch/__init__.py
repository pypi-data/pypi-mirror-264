from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PlcchCls:
	"""Plcch commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("plcch", core, parent)

	@property
	def ssPattern(self):
		"""ssPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssPattern'):
			from .SsPattern import SsPatternCls
			self._ssPattern = SsPatternCls(self._core, self._cmd_group)
		return self._ssPattern

	@property
	def tpcPattern(self):
		"""tpcPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcPattern'):
			from .TpcPattern import TpcPatternCls
			self._tpcPattern = TpcPatternCls(self._core, self._cmd_group)
		return self._tpcPattern

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .TtInterval import TtIntervalCls
			self._ttInterval = TtIntervalCls(self._core, self._cmd_group)
		return self._ttInterval

	def clone(self) -> 'PlcchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PlcchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
