from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RctrlCls:
	"""Rctrl commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rctrl", core, parent)

	@property
	def cperiod(self):
		"""cperiod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cperiod'):
			from .Cperiod import CperiodCls
			self._cperiod = CperiodCls(self._core, self._cmd_group)
		return self._cperiod

	@property
	def offsetInd(self):
		"""offsetInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offsetInd'):
			from .OffsetInd import OffsetIndCls
			self._offsetInd = OffsetIndCls(self._core, self._cmd_group)
		return self._offsetInd

	@property
	def prbNumber(self):
		"""prbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbNumber'):
			from .PrbNumber import PrbNumberCls
			self._prbNumber = PrbNumberCls(self._core, self._cmd_group)
		return self._prbNumber

	@property
	def prbStart(self):
		"""prbStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbStart'):
			from .PrbStart import PrbStartCls
			self._prbStart = PrbStartCls(self._core, self._cmd_group)
		return self._prbStart

	@property
	def prend(self):
		"""prend commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prend'):
			from .Prend import PrendCls
			self._prend = PrendCls(self._core, self._cmd_group)
		return self._prend

	@property
	def sfbmp(self):
		"""sfbmp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfbmp'):
			from .Sfbmp import SfbmpCls
			self._sfbmp = SfbmpCls(self._core, self._cmd_group)
		return self._sfbmp

	def clone(self) -> 'RctrlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RctrlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
