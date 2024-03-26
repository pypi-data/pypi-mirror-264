from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HschCls:
	"""Hsch commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hsch", core, parent)

	@property
	def cvpb(self):
		"""cvpb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cvpb'):
			from .Cvpb import CvpbCls
			self._cvpb = CvpbCls(self._core, self._cmd_group)
		return self._cvpb

	@property
	def prsr(self):
		"""prsr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prsr'):
			from .Prsr import PrsrCls
			self._prsr = PrsrCls(self._core, self._cmd_group)
		return self._prsr

	@property
	def psbs(self):
		"""psbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psbs'):
			from .Psbs import PsbsCls
			self._psbs = PsbsCls(self._core, self._cmd_group)
		return self._psbs

	@property
	def rvParameter(self):
		"""rvParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvParameter'):
			from .RvParameter import RvParameterCls
			self._rvParameter = RvParameterCls(self._core, self._cmd_group)
		return self._rvParameter

	def clone(self) -> 'HschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
