from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UciCls:
	"""Uci commands group definition. 9 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uci", core, parent)

	@property
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Bits import BitsCls
			self._bits = BitsCls(self._core, self._cmd_group)
		return self._bits

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Crate import CrateCls
			self._crate = CrateCls(self._core, self._cmd_group)
		return self._crate

	@property
	def cs1Bits(self):
		"""cs1Bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs1Bits'):
			from .Cs1Bits import Cs1BitsCls
			self._cs1Bits = Cs1BitsCls(self._core, self._cmd_group)
		return self._cs1Bits

	@property
	def cs1Pattern(self):
		"""cs1Pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs1Pattern'):
			from .Cs1Pattern import Cs1PatternCls
			self._cs1Pattern = Cs1PatternCls(self._core, self._cmd_group)
		return self._cs1Pattern

	@property
	def cs2Bits(self):
		"""cs2Bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs2Bits'):
			from .Cs2Bits import Cs2BitsCls
			self._cs2Bits = Cs2BitsCls(self._core, self._cmd_group)
		return self._cs2Bits

	@property
	def cs2Pattern(self):
		"""cs2Pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs2Pattern'):
			from .Cs2Pattern import Cs2PatternCls
			self._cs2Pattern = Cs2PatternCls(self._core, self._cmd_group)
		return self._cs2Pattern

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def srpt(self):
		"""srpt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srpt'):
			from .Srpt import SrptCls
			self._srpt = SrptCls(self._core, self._cmd_group)
		return self._srpt

	def clone(self) -> 'UciCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UciCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
