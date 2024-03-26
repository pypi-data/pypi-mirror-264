from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcodingCls:
	"""Ccoding commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ccoding", core, parent)

	@property
	def frcr(self):
		"""frcr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frcr'):
			from .Frcr import FrcrCls
			self._frcr = FrcrCls(self._core, self._cmd_group)
		return self._frcr

	@property
	def rvIndex(self):
		"""rvIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvIndex'):
			from .RvIndex import RvIndexCls
			self._rvIndex = RvIndexCls(self._core, self._cmd_group)
		return self._rvIndex

	@property
	def tbsFactor(self):
		"""tbsFactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbsFactor'):
			from .TbsFactor import TbsFactorCls
			self._tbsFactor = TbsFactorCls(self._core, self._cmd_group)
		return self._tbsFactor

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .TbSize import TbSizeCls
			self._tbSize = TbSizeCls(self._core, self._cmd_group)
		return self._tbSize

	@property
	def tcRate(self):
		"""tcRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcRate'):
			from .TcRate import TcRateCls
			self._tcRate = TcRateCls(self._core, self._cmd_group)
		return self._tcRate

	def clone(self) -> 'CcodingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CcodingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
