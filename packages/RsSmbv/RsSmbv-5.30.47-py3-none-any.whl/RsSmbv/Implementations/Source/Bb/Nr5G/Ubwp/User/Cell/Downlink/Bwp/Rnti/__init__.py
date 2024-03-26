from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RntiCls:
	"""Rnti commands group definition. 7 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rnti", core, parent)

	@property
	def aiRnti(self):
		"""aiRnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aiRnti'):
			from .AiRnti import AiRntiCls
			self._aiRnti = AiRntiCls(self._core, self._cmd_group)
		return self._aiRnti

	@property
	def ciRnti(self):
		"""ciRnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ciRnti'):
			from .CiRnti import CiRntiCls
			self._ciRnti = CiRntiCls(self._core, self._cmd_group)
		return self._ciRnti

	@property
	def int(self):
		"""int commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_int'):
			from .Int import IntCls
			self._int = IntCls(self._core, self._cmd_group)
		return self._int

	@property
	def psRnti(self):
		"""psRnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psRnti'):
			from .PsRnti import PsRntiCls
			self._psRnti = PsRntiCls(self._core, self._cmd_group)
		return self._psRnti

	@property
	def pucch(self):
		"""pucch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pucch'):
			from .Pucch import PucchCls
			self._pucch = PucchCls(self._core, self._cmd_group)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	@property
	def srs(self):
		"""srs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srs'):
			from .Srs import SrsCls
			self._srs = SrsCls(self._core, self._cmd_group)
		return self._srs

	def clone(self) -> 'RntiCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RntiCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
