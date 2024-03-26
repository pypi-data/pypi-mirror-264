from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 8 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	@property
	def meandering(self):
		"""meandering commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_meandering'):
			from .Meandering import MeanderingCls
			self._meandering = MeanderingCls(self._core, self._cmd_group)
		return self._meandering

	@property
	def nmessage(self):
		"""nmessage commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmessage'):
			from .Nmessage import NmessageCls
			self._nmessage = NmessageCls(self._core, self._cmd_group)
		return self._nmessage

	@property
	def pcode(self):
		"""pcode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcode'):
			from .Pcode import PcodeCls
			self._pcode = PcodeCls(self._core, self._cmd_group)
		return self._pcode

	@property
	def tsequence(self):
		"""tsequence commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsequence'):
			from .Tsequence import TsequenceCls
			self._tsequence = TsequenceCls(self._core, self._cmd_group)
		return self._tsequence

	def clone(self) -> 'DataCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DataCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
