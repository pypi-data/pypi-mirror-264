from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApMapCls:
	"""ApMap commands group definition. 13 total commands, 13 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apMap", core, parent)

	@property
	def ap1000Map(self):
		"""ap1000Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap1000Map'):
			from .Ap1000Map import Ap1000MapCls
			self._ap1000Map = Ap1000MapCls(self._core, self._cmd_group)
		return self._ap1000Map

	@property
	def ap100Map(self):
		"""ap100Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap100Map'):
			from .Ap100Map import Ap100MapCls
			self._ap100Map = Ap100MapCls(self._core, self._cmd_group)
		return self._ap100Map

	@property
	def ap1010Map(self):
		"""ap1010Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap1010Map'):
			from .Ap1010Map import Ap1010MapCls
			self._ap1010Map = Ap1010MapCls(self._core, self._cmd_group)
		return self._ap1010Map

	@property
	def ap1020Map(self):
		"""ap1020Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap1020Map'):
			from .Ap1020Map import Ap1020MapCls
			self._ap1020Map = Ap1020MapCls(self._core, self._cmd_group)
		return self._ap1020Map

	@property
	def ap10Map(self):
		"""ap10Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap10Map'):
			from .Ap10Map import Ap10MapCls
			self._ap10Map = Ap10MapCls(self._core, self._cmd_group)
		return self._ap10Map

	@property
	def ap200Map(self):
		"""ap200Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap200Map'):
			from .Ap200Map import Ap200MapCls
			self._ap200Map = Ap200MapCls(self._core, self._cmd_group)
		return self._ap200Map

	@property
	def ap201Map(self):
		"""ap201Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap201Map'):
			from .Ap201Map import Ap201MapCls
			self._ap201Map = Ap201MapCls(self._core, self._cmd_group)
		return self._ap201Map

	@property
	def ap20Map(self):
		"""ap20Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap20Map'):
			from .Ap20Map import Ap20MapCls
			self._ap20Map = Ap20MapCls(self._core, self._cmd_group)
		return self._ap20Map

	@property
	def ap21Map(self):
		"""ap21Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap21Map'):
			from .Ap21Map import Ap21MapCls
			self._ap21Map = Ap21MapCls(self._core, self._cmd_group)
		return self._ap21Map

	@property
	def ap40Map(self):
		"""ap40Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap40Map'):
			from .Ap40Map import Ap40MapCls
			self._ap40Map = Ap40MapCls(self._core, self._cmd_group)
		return self._ap40Map

	@property
	def ap41Map(self):
		"""ap41Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap41Map'):
			from .Ap41Map import Ap41MapCls
			self._ap41Map = Ap41MapCls(self._core, self._cmd_group)
		return self._ap41Map

	@property
	def ap42Map(self):
		"""ap42Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap42Map'):
			from .Ap42Map import Ap42MapCls
			self._ap42Map = Ap42MapCls(self._core, self._cmd_group)
		return self._ap42Map

	@property
	def ap43Map(self):
		"""ap43Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap43Map'):
			from .Ap43Map import Ap43MapCls
			self._ap43Map = Ap43MapCls(self._core, self._cmd_group)
		return self._ap43Map

	def clone(self) -> 'ApMapCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApMapCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
