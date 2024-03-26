from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcodingCls:
	"""Ccoding commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ccoding", core, parent)

	@property
	def isbSize(self):
		"""isbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isbSize'):
			from .IsbSize import IsbSizeCls
			self._isbSize = IsbSizeCls(self._core, self._cmd_group)
		return self._isbSize

	@property
	def rvIndex(self):
		"""rvIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvIndex'):
			from .RvIndex import RvIndexCls
			self._rvIndex = RvIndexCls(self._core, self._cmd_group)
		return self._rvIndex

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .TbSize import TbSizeCls
			self._tbSize = TbSizeCls(self._core, self._cmd_group)
		return self._tbSize

	def clone(self) -> 'CcodingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CcodingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
