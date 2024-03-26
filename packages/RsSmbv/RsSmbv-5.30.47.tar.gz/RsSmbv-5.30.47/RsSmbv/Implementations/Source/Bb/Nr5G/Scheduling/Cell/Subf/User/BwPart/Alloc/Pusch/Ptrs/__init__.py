from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtrsCls:
	"""Ptrs commands group definition. 14 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptrs", core, parent)

	@property
	def frqDen(self):
		"""frqDen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frqDen'):
			from .FrqDen import FrqDenCls
			self._frqDen = FrqDenCls(self._core, self._cmd_group)
		return self._frqDen

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def port(self):
		"""port commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_port'):
			from .Port import PortCls
			self._port = PortCls(self._core, self._cmd_group)
		return self._port

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def ptdmrs(self):
		"""ptdmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptdmrs'):
			from .Ptdmrs import PtdmrsCls
			self._ptdmrs = PtdmrsCls(self._core, self._cmd_group)
		return self._ptdmrs

	@property
	def reof(self):
		"""reof commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reof'):
			from .Reof import ReofCls
			self._reof = ReofCls(self._core, self._cmd_group)
		return self._reof

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tmDen(self):
		"""tmDen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmDen'):
			from .TmDen import TmDenCls
			self._tmDen = TmDenCls(self._core, self._cmd_group)
		return self._tmDen

	@property
	def tp(self):
		"""tp commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_tp'):
			from .Tp import TpCls
			self._tp = TpCls(self._core, self._cmd_group)
		return self._tp

	def clone(self) -> 'PtrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PtrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
