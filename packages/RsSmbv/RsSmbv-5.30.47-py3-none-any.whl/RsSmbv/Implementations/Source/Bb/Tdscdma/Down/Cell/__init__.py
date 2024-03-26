from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CellCls:
	"""Cell commands group definition. 142 total commands, 12 Subgroups, 0 group commands
	Repeated Capability: Cell, default value after init: Cell.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cell", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_cell_get', 'repcap_cell_set', repcap.Cell.Nr1)

	def repcap_cell_set(self, cell: repcap.Cell) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Cell.Default
		Default value after init: Cell.Nr1"""
		self._cmd_group.set_repcap_enum_value(cell)

	def repcap_cell_get(self) -> repcap.Cell:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def dwpts(self):
		"""dwpts commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dwpts'):
			from .Dwpts import DwptsCls
			self._dwpts = DwptsCls(self._core, self._cmd_group)
		return self._dwpts

	@property
	def enh(self):
		"""enh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_enh'):
			from .Enh import EnhCls
			self._enh = EnhCls(self._core, self._cmd_group)
		return self._enh

	@property
	def mcode(self):
		"""mcode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcode'):
			from .Mcode import McodeCls
			self._mcode = McodeCls(self._core, self._cmd_group)
		return self._mcode

	@property
	def protation(self):
		"""protation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_protation'):
			from .Protation import ProtationCls
			self._protation = ProtationCls(self._core, self._cmd_group)
		return self._protation

	@property
	def scode(self):
		"""scode commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Scode import ScodeCls
			self._scode = ScodeCls(self._core, self._cmd_group)
		return self._scode

	@property
	def sdCode(self):
		"""sdCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sdCode'):
			from .SdCode import SdCodeCls
			self._sdCode = SdCodeCls(self._core, self._cmd_group)
		return self._sdCode

	@property
	def slot(self):
		"""slot commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .Slot import SlotCls
			self._slot = SlotCls(self._core, self._cmd_group)
		return self._slot

	@property
	def spoint(self):
		"""spoint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spoint'):
			from .Spoint import SpointCls
			self._spoint = SpointCls(self._core, self._cmd_group)
		return self._spoint

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def suCode(self):
		"""suCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_suCode'):
			from .SuCode import SuCodeCls
			self._suCode = SuCodeCls(self._core, self._cmd_group)
		return self._suCode

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Tdelay import TdelayCls
			self._tdelay = TdelayCls(self._core, self._cmd_group)
		return self._tdelay

	@property
	def users(self):
		"""users commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_users'):
			from .Users import UsersCls
			self._users = UsersCls(self._core, self._cmd_group)
		return self._users

	def clone(self) -> 'CellCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CellCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
