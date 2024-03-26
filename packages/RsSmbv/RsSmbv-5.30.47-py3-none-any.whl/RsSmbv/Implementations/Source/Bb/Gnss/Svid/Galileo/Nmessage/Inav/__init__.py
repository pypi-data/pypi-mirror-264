from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InavCls:
	"""Inav commands group definition. 49 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inav", core, parent)

	@property
	def ccorrection(self):
		"""ccorrection commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccorrection'):
			from .Ccorrection import CcorrectionCls
			self._ccorrection = CcorrectionCls(self._core, self._cmd_group)
		return self._ccorrection

	@property
	def e1Bdvs(self):
		"""e1Bdvs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e1Bdvs'):
			from .E1Bdvs import E1BdvsCls
			self._e1Bdvs = E1BdvsCls(self._core, self._cmd_group)
		return self._e1Bdvs

	@property
	def e1Bhs(self):
		"""e1Bhs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e1Bhs'):
			from .E1Bhs import E1BhsCls
			self._e1Bhs = E1BhsCls(self._core, self._cmd_group)
		return self._e1Bhs

	@property
	def e5Bdvs(self):
		"""e5Bdvs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Bdvs'):
			from .E5Bdvs import E5BdvsCls
			self._e5Bdvs = E5BdvsCls(self._core, self._cmd_group)
		return self._e5Bdvs

	@property
	def e5Bhs(self):
		"""e5Bhs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e5Bhs'):
			from .E5Bhs import E5BhsCls
			self._e5Bhs = E5BhsCls(self._core, self._cmd_group)
		return self._e5Bhs

	@property
	def ephemeris(self):
		"""ephemeris commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_ephemeris'):
			from .Ephemeris import EphemerisCls
			self._ephemeris = EphemerisCls(self._core, self._cmd_group)
		return self._ephemeris

	def clone(self) -> 'InavCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InavCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
