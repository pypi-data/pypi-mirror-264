from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HsdpaCls:
	"""Hsdpa commands group definition. 48 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hsdpa", core, parent)

	@property
	def bmode(self):
		"""bmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bmode'):
			from .Bmode import BmodeCls
			self._bmode = BmodeCls(self._core, self._cmd_group)
		return self._bmode

	@property
	def cvpb(self):
		"""cvpb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cvpb'):
			from .Cvpb import CvpbCls
			self._cvpb = CvpbCls(self._core, self._cmd_group)
		return self._cvpb

	@property
	def hset(self):
		"""hset commands group. 29 Sub-classes, 2 commands."""
		if not hasattr(self, '_hset'):
			from .Hset import HsetCls
			self._hset = HsetCls(self._core, self._cmd_group)
		return self._hset

	@property
	def mimo(self):
		"""mimo commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .Mimo import MimoCls
			self._mimo = MimoCls(self._core, self._cmd_group)
		return self._mimo

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

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
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def ttiDistance(self):
		"""ttiDistance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiDistance'):
			from .TtiDistance import TtiDistanceCls
			self._ttiDistance = TtiDistanceCls(self._core, self._cmd_group)
		return self._ttiDistance

	def clone(self) -> 'HsdpaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HsdpaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
