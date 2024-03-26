from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrErrorsCls:
	"""PrErrors commands group definition. 12 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prErrors", core, parent)

	@property
	def copy(self):
		"""copy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_copy'):
			from .Copy import CopyCls
			self._copy = CopyCls(self._core, self._cmd_group)
		return self._copy

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def profile(self):
		"""profile commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_profile'):
			from .Profile import ProfileCls
			self._profile = ProfileCls(self._core, self._cmd_group)
		return self._profile

	@property
	def value(self):
		"""value commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_value'):
			from .Value import ValueCls
			self._value = ValueCls(self._core, self._cmd_group)
		return self._value

	def clone(self) -> 'PrErrorsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PrErrorsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
