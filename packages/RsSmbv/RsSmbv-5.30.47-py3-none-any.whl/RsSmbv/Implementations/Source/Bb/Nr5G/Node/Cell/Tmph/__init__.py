from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TmphCls:
	"""Tmph commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tmph", core, parent)

	@property
	def ctOffset(self):
		"""ctOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctOffset'):
			from .CtOffset import CtOffsetCls
			self._ctOffset = CtOffsetCls(self._core, self._cmd_group)
		return self._ctOffset

	@property
	def phOffset(self):
		"""phOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phOffset'):
			from .PhOffset import PhOffsetCls
			self._phOffset = PhOffsetCls(self._core, self._cmd_group)
		return self._phOffset

	@property
	def sfOffset(self):
		"""sfOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfOffset'):
			from .SfOffset import SfOffsetCls
			self._sfOffset = SfOffsetCls(self._core, self._cmd_group)
		return self._sfOffset

	@property
	def ssbtOffset(self):
		"""ssbtOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssbtOffset'):
			from .SsbtOffset import SsbtOffsetCls
			self._ssbtOffset = SsbtOffsetCls(self._core, self._cmd_group)
		return self._ssbtOffset

	@property
	def syfnOffset(self):
		"""syfnOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_syfnOffset'):
			from .SyfnOffset import SyfnOffsetCls
			self._syfnOffset = SyfnOffsetCls(self._core, self._cmd_group)
		return self._syfnOffset

	@property
	def taOffset(self):
		"""taOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taOffset'):
			from .TaOffset import TaOffsetCls
			self._taOffset = TaOffsetCls(self._core, self._cmd_group)
		return self._taOffset

	def clone(self) -> 'TmphCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TmphCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
