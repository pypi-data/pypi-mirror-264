from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpchCls:
	"""Dpch commands group definition. 36 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpch", core, parent)

	@property
	def ccoding(self):
		"""ccoding commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Ccoding import CcodingCls
			self._ccoding = CcodingCls(self._core, self._cmd_group)
		return self._ccoding

	@property
	def derror(self):
		"""derror commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_derror'):
			from .Derror import DerrorCls
			self._derror = DerrorCls(self._core, self._cmd_group)
		return self._derror

	@property
	def dpControl(self):
		"""dpControl commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpControl'):
			from .DpControl import DpControlCls
			self._dpControl = DpControlCls(self._core, self._cmd_group)
		return self._dpControl

	@property
	def interleaver2(self):
		"""interleaver2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interleaver2'):
			from .Interleaver2 import Interleaver2Cls
			self._interleaver2 = Interleaver2Cls(self._core, self._cmd_group)
		return self._interleaver2

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tchannel(self):
		"""tchannel commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_tchannel'):
			from .Tchannel import TchannelCls
			self._tchannel = TchannelCls(self._core, self._cmd_group)
		return self._tchannel

	def clone(self) -> 'DpchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
