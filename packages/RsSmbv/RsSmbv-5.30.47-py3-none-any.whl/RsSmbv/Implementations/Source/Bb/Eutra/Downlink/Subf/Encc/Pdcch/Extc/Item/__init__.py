from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ItemCls:
	"""Item commands group definition. 57 total commands, 12 Subgroups, 0 group commands
	Repeated Capability: ItemNull, default value after init: ItemNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("item", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_itemNull_get', 'repcap_itemNull_set', repcap.ItemNull.Nr0)

	def repcap_itemNull_set(self, itemNull: repcap.ItemNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ItemNull.Default
		Default value after init: ItemNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(itemNull)

	def repcap_itemNull_get(self) -> repcap.ItemNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cell(self):
		"""cell commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	@property
	def cindex(self):
		"""cindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cindex'):
			from .Cindex import CindexCls
			self._cindex = CindexCls(self._core, self._cmd_group)
		return self._cindex

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Conflict import ConflictCls
			self._conflict = ConflictCls(self._core, self._cmd_group)
		return self._conflict

	@property
	def dciConf(self):
		"""dciConf commands group. 37 Sub-classes, 0 commands."""
		if not hasattr(self, '_dciConf'):
			from .DciConf import DciConfCls
			self._dciConf = DciConfCls(self._core, self._cmd_group)
		return self._dciConf

	@property
	def dciFmt(self):
		"""dciFmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dciFmt'):
			from .DciFmt import DciFmtCls
			self._dciFmt = DciFmtCls(self._core, self._cmd_group)
		return self._dciFmt

	@property
	def ncces(self):
		"""ncces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncces'):
			from .Ncces import NccesCls
			self._ncces = NccesCls(self._core, self._cmd_group)
		return self._ncces

	@property
	def ndcces(self):
		"""ndcces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndcces'):
			from .Ndcces import NdccesCls
			self._ndcces = NdccesCls(self._core, self._cmd_group)
		return self._ndcces

	@property
	def pdcchType(self):
		"""pdcchType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdcchType'):
			from .PdcchType import PdcchTypeCls
			self._pdcchType = PdcchTypeCls(self._core, self._cmd_group)
		return self._pdcchType

	@property
	def pfmt(self):
		"""pfmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfmt'):
			from .Pfmt import PfmtCls
			self._pfmt = PfmtCls(self._core, self._cmd_group)
		return self._pfmt

	@property
	def sespace(self):
		"""sespace commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_sespace'):
			from .Sespace import SespaceCls
			self._sespace = SespaceCls(self._core, self._cmd_group)
		return self._sespace

	@property
	def ueId(self):
		"""ueId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueId'):
			from .UeId import UeIdCls
			self._ueId = UeIdCls(self._core, self._cmd_group)
		return self._ueId

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'ItemCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ItemCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
