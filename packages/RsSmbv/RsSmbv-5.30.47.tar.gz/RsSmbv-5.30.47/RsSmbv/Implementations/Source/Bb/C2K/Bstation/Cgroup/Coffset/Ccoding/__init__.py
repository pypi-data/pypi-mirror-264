from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcodingCls:
	"""Ccoding commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ccoding", core, parent)

	@property
	def binterleaver(self):
		"""binterleaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_binterleaver'):
			from .Binterleaver import BinterleaverCls
			self._binterleaver = BinterleaverCls(self._core, self._cmd_group)
		return self._binterleaver

	@property
	def bitFrame(self):
		"""bitFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitFrame'):
			from .BitFrame import BitFrameCls
			self._bitFrame = BitFrameCls(self._core, self._cmd_group)
		return self._bitFrame

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Crc import CrcCls
			self._crc = CrcCls(self._core, self._cmd_group)
		return self._crc

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def spuncture(self):
		"""spuncture commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spuncture'):
			from .Spuncture import SpunctureCls
			self._spuncture = SpunctureCls(self._core, self._cmd_group)
		return self._spuncture

	@property
	def srepetition(self):
		"""srepetition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srepetition'):
			from .Srepetition import SrepetitionCls
			self._srepetition = SrepetitionCls(self._core, self._cmd_group)
		return self._srepetition

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'CcodingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CcodingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
