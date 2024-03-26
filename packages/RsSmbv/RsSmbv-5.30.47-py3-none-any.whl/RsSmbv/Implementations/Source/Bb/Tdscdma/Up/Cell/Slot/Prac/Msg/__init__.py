from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MsgCls:
	"""Msg commands group definition. 12 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("msg", core, parent)

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Length import LengthCls
			self._length = LengthCls(self._core, self._cmd_group)
		return self._length

	@property
	def mshift(self):
		"""mshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mshift'):
			from .Mshift import MshiftCls
			self._mshift = MshiftCls(self._core, self._cmd_group)
		return self._mshift

	@property
	def pcorrection(self):
		"""pcorrection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcorrection'):
			from .Pcorrection import PcorrectionCls
			self._pcorrection = PcorrectionCls(self._core, self._cmd_group)
		return self._pcorrection

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def scode(self):
		"""scode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Scode import ScodeCls
			self._scode = ScodeCls(self._core, self._cmd_group)
		return self._scode

	@property
	def sfactor(self):
		"""sfactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfactor'):
			from .Sfactor import SfactorCls
			self._sfactor = SfactorCls(self._core, self._cmd_group)
		return self._sfactor

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'MsgCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MsgCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
