from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CmCls:
	"""Cm commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cm", core, parent)

	@property
	def imaginary(self):
		"""imaginary commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imaginary'):
			from .Imaginary import ImaginaryCls
			self._imaginary = ImaginaryCls(self._core, self._cmd_group)
		return self._imaginary

	@property
	def magnitude(self):
		"""magnitude commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_magnitude'):
			from .Magnitude import MagnitudeCls
			self._magnitude = MagnitudeCls(self._core, self._cmd_group)
		return self._magnitude

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def real(self):
		"""real commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_real'):
			from .Real import RealCls
			self._real = RealCls(self._core, self._cmd_group)
		return self._real

	def clone(self) -> 'CmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
