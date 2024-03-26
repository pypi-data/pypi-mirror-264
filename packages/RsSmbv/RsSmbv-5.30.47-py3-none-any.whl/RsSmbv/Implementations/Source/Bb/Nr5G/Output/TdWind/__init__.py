from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TdWindCls:
	"""TdWind commands group definition. 22 total commands, 11 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tdWind", core, parent)

	@property
	def s120K(self):
		"""s120K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_s120K'):
			from .S120K import S120KCls
			self._s120K = S120KCls(self._core, self._cmd_group)
		return self._s120K

	@property
	def s15K(self):
		"""s15K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_s15K'):
			from .S15K import S15KCls
			self._s15K = S15KCls(self._core, self._cmd_group)
		return self._s15K

	@property
	def s240K(self):
		"""s240K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_s240K'):
			from .S240K import S240KCls
			self._s240K = S240KCls(self._core, self._cmd_group)
		return self._s240K

	@property
	def s30K(self):
		"""s30K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_s30K'):
			from .S30K import S30KCls
			self._s30K = S30KCls(self._core, self._cmd_group)
		return self._s30K

	@property
	def s60K(self):
		"""s60K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_s60K'):
			from .S60K import S60KCls
			self._s60K = S60KCls(self._core, self._cmd_group)
		return self._s60K

	@property
	def se60K(self):
		"""se60K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_se60K'):
			from .Se60K import Se60KCls
			self._se60K = Se60KCls(self._core, self._cmd_group)
		return self._se60K

	@property
	def sp120K(self):
		"""sp120K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sp120K'):
			from .Sp120K import Sp120KCls
			self._sp120K = Sp120KCls(self._core, self._cmd_group)
		return self._sp120K

	@property
	def sp15K(self):
		"""sp15K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sp15K'):
			from .Sp15K import Sp15KCls
			self._sp15K = Sp15KCls(self._core, self._cmd_group)
		return self._sp15K

	@property
	def sp30K(self):
		"""sp30K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sp30K'):
			from .Sp30K import Sp30KCls
			self._sp30K = Sp30KCls(self._core, self._cmd_group)
		return self._sp30K

	@property
	def sp5K(self):
		"""sp5K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sp5K'):
			from .Sp5K import Sp5KCls
			self._sp5K = Sp5KCls(self._core, self._cmd_group)
		return self._sp5K

	@property
	def sp60K(self):
		"""sp60K commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sp60K'):
			from .Sp60K import Sp60KCls
			self._sp60K = Sp60KCls(self._core, self._cmd_group)
		return self._sp60K

	def clone(self) -> 'TdWindCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TdWindCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
