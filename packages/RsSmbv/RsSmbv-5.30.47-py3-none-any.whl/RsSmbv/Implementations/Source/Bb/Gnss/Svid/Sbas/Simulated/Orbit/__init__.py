from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OrbitCls:
	"""Orbit commands group definition. 11 total commands, 11 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("orbit", core, parent)

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .Date import DateCls
			self._date = DateCls(self._core, self._cmd_group)
		return self._date

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def xddn(self):
		"""xddn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xddn'):
			from .Xddn import XddnCls
			self._xddn = XddnCls(self._core, self._cmd_group)
		return self._xddn

	@property
	def xdn(self):
		"""xdn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xdn'):
			from .Xdn import XdnCls
			self._xdn = XdnCls(self._core, self._cmd_group)
		return self._xdn

	@property
	def xn(self):
		"""xn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xn'):
			from .Xn import XnCls
			self._xn = XnCls(self._core, self._cmd_group)
		return self._xn

	@property
	def yddn(self):
		"""yddn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yddn'):
			from .Yddn import YddnCls
			self._yddn = YddnCls(self._core, self._cmd_group)
		return self._yddn

	@property
	def ydn(self):
		"""ydn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ydn'):
			from .Ydn import YdnCls
			self._ydn = YdnCls(self._core, self._cmd_group)
		return self._ydn

	@property
	def yn(self):
		"""yn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yn'):
			from .Yn import YnCls
			self._yn = YnCls(self._core, self._cmd_group)
		return self._yn

	@property
	def zddn(self):
		"""zddn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zddn'):
			from .Zddn import ZddnCls
			self._zddn = ZddnCls(self._core, self._cmd_group)
		return self._zddn

	@property
	def zdn(self):
		"""zdn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zdn'):
			from .Zdn import ZdnCls
			self._zdn = ZdnCls(self._core, self._cmd_group)
		return self._zdn

	@property
	def zn(self):
		"""zn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zn'):
			from .Zn import ZnCls
			self._zn = ZnCls(self._core, self._cmd_group)
		return self._zn

	def clone(self) -> 'OrbitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OrbitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
