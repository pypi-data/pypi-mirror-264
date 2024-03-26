from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyInfoCls:
	"""SyInfo commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("syInfo", core, parent)

	@property
	def hacbook(self):
		"""hacbook commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hacbook'):
			from .Hacbook import HacbookCls
			self._hacbook = HacbookCls(self._core, self._cmd_group)
		return self._hacbook

	@property
	def hacr(self):
		"""hacr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hacr'):
			from .Hacr import HacrCls
			self._hacr = HacrCls(self._core, self._cmd_group)
		return self._hacr

	@property
	def indSize(self):
		"""indSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indSize'):
			from .IndSize import IndSizeCls
			self._indSize = IndSizeCls(self._core, self._cmd_group)
		return self._indSize

	@property
	def is02(self):
		"""is02 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_is02'):
			from .Is02 import Is02Cls
			self._is02 = Is02Cls(self._core, self._cmd_group)
		return self._is02

	@property
	def sul(self):
		"""sul commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sul'):
			from .Sul import SulCls
			self._sul = SulCls(self._core, self._cmd_group)
		return self._sul

	def clone(self) -> 'SyInfoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SyInfoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
