from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PucchCls:
	"""Pucch commands group definition. 24 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pucch", core, parent)

	@property
	def fs(self):
		"""fs commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_fs'):
			from .Fs import FsCls
			self._fs = FsCls(self._core, self._cmd_group)
		return self._fs

	@property
	def grpHopping(self):
		"""grpHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_grpHopping'):
			from .GrpHopping import GrpHoppingCls
			self._grpHopping = GrpHoppingCls(self._core, self._cmd_group)
		return self._grpHopping

	@property
	def hopId(self):
		"""hopId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopId'):
			from .HopId import HopIdCls
			self._hopId = HopIdCls(self._core, self._cmd_group)
		return self._hopId

	@property
	def int(self):
		"""int commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_int'):
			from .Int import IntCls
			self._int = IntCls(self._core, self._cmd_group)
		return self._int

	@property
	def isfHopping(self):
		"""isfHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isfHopping'):
			from .IsfHopping import IsfHoppingCls
			self._isfHopping = IsfHoppingCls(self._core, self._cmd_group)
		return self._isfHopping

	@property
	def nint(self):
		"""nint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nint'):
			from .Nint import NintCls
			self._nint = NintCls(self._core, self._cmd_group)
		return self._nint

	@property
	def pl(self):
		"""pl commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pl'):
			from .Pl import PlCls
			self._pl = PlCls(self._core, self._cmd_group)
		return self._pl

	@property
	def shopping(self):
		"""shopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shopping'):
			from .Shopping import ShoppingCls
			self._shopping = ShoppingCls(self._core, self._cmd_group)
		return self._shopping

	def clone(self) -> 'PucchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PucchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
