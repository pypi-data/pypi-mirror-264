from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1BandCls:
	"""L1Band commands group definition. 58 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l1Band", core, parent)

	@property
	def c1C(self):
		"""c1C commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_c1C'):
			from .C1C import C1CCls
			self._c1C = C1CCls(self._core, self._cmd_group)
		return self._c1C

	@property
	def c2C(self):
		"""c2C commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_c2C'):
			from .C2C import C2CCls
			self._c2C = C2CCls(self._core, self._cmd_group)
		return self._c2C

	@property
	def ca(self):
		"""ca commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ca'):
			from .Ca import CaCls
			self._ca = CaCls(self._core, self._cmd_group)
		return self._ca

	@property
	def l1C(self):
		"""l1C commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1C'):
			from .L1C import L1CCls
			self._l1C = L1CCls(self._core, self._cmd_group)
		return self._l1C

	@property
	def m(self):
		"""m commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_m'):
			from .M import MCls
			self._m = MCls(self._core, self._cmd_group)
		return self._m

	@property
	def p(self):
		"""p commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_p'):
			from .P import PCls
			self._p = PCls(self._core, self._cmd_group)
		return self._p

	@property
	def py(self):
		"""py commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_py'):
			from .Py import PyCls
			self._py = PyCls(self._core, self._cmd_group)
		return self._py

	def clone(self) -> 'L1BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L1BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
