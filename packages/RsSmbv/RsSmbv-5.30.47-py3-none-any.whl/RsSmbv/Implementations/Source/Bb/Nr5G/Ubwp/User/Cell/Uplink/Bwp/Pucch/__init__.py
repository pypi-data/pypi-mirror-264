from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PucchCls:
	"""Pucch commands group definition. 12 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pucch", core, parent)

	@property
	def a12List(self):
		"""a12List commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_a12List'):
			from .A12List import A12ListCls
			self._a12List = A12ListCls(self._core, self._cmd_group)
		return self._a12List

	@property
	def adMrs(self):
		"""adMrs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adMrs'):
			from .AdMrs import AdMrsCls
			self._adMrs = AdMrsCls(self._core, self._cmd_group)
		return self._adMrs

	@property
	def bpsk(self):
		"""bpsk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpsk'):
			from .Bpsk import BpskCls
			self._bpsk = BpskCls(self._core, self._cmd_group)
		return self._bpsk

	@property
	def brind(self):
		"""brind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_brind'):
			from .Brind import BrindCls
			self._brind = BrindCls(self._core, self._cmd_group)
		return self._brind

	@property
	def cpext(self):
		"""cpext commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cpext'):
			from .Cpext import CpextCls
			self._cpext = CpextCls(self._core, self._cmd_group)
		return self._cpext

	@property
	def hack(self):
		"""hack commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hack'):
			from .Hack import HackCls
			self._hack = HackCls(self._core, self._cmd_group)
		return self._hack

	@property
	def pdsharq(self):
		"""pdsharq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsharq'):
			from .Pdsharq import PdsharqCls
			self._pdsharq = PdsharqCls(self._core, self._cmd_group)
		return self._pdsharq

	@property
	def u2Tpc(self):
		"""u2Tpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_u2Tpc'):
			from .U2Tpc import U2TpcCls
			self._u2Tpc = U2TpcCls(self._core, self._cmd_group)
		return self._u2Tpc

	@property
	def uitl(self):
		"""uitl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uitl'):
			from .Uitl import UitlCls
			self._uitl = UitlCls(self._core, self._cmd_group)
		return self._uitl

	@property
	def ur16(self):
		"""ur16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ur16'):
			from .Ur16 import Ur16Cls
			self._ur16 = Ur16Cls(self._core, self._cmd_group)
		return self._ur16

	def clone(self) -> 'PucchCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PucchCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
