from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DgCls:
	"""Dg commands group definition. 16 total commands, 12 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dg", core, parent)

	@property
	def ccgp(self):
		"""ccgp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccgp'):
			from .Ccgp import CcgpCls
			self._ccgp = CcgpCls(self._core, self._cmd_group)
		return self._ccgp

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def gpolynomial(self):
		"""gpolynomial commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gpolynomial'):
			from .Gpolynomial import GpolynomialCls
			self._gpolynomial = GpolynomialCls(self._core, self._cmd_group)
		return self._gpolynomial

	@property
	def m11state(self):
		"""m11state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_m11state'):
			from .M11state import M11stateCls
			self._m11state = M11stateCls(self._core, self._cmd_group)
		return self._m11state

	@property
	def m1state(self):
		"""m1state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_m1state'):
			from .M1state import M1stateCls
			self._m1state = M1stateCls(self._core, self._cmd_group)
		return self._m1state

	@property
	def predefined(self):
		"""predefined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	@property
	def rbOrder(self):
		"""rbOrder commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rbOrder'):
			from .RbOrder import RbOrderCls
			self._rbOrder = RbOrderCls(self._core, self._cmd_group)
		return self._rbOrder

	@property
	def sfile(self):
		"""sfile commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfile'):
			from .Sfile import SfileCls
			self._sfile = SfileCls(self._core, self._cmd_group)
		return self._sfile

	@property
	def spredefined(self):
		"""spredefined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_spredefined'):
			from .Spredefined import SpredefinedCls
			self._spredefined = SpredefinedCls(self._core, self._cmd_group)
		return self._spredefined

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def suser(self):
		"""suser commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_suser'):
			from .Suser import SuserCls
			self._suser = SuserCls(self._core, self._cmd_group)
		return self._suser

	@property
	def user(self):
		"""user commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'DgCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DgCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
