from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BlockCls:
	"""Block commands group definition. 5 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: FmBlock, default value after init: FmBlock.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("block", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_fmBlock_get', 'repcap_fmBlock_set', repcap.FmBlock.Nr1)

	def repcap_fmBlock_set(self, fmBlock: repcap.FmBlock) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FmBlock.Default
		Default value after init: FmBlock.Nr1"""
		self._cmd_group.set_repcap_enum_value(fmBlock)

	def repcap_fmBlock_get(self) -> repcap.FmBlock:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def bdata(self):
		"""bdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bdata'):
			from .Bdata import BdataCls
			self._bdata = BdataCls(self._core, self._cmd_group)
		return self._bdata

	@property
	def bnumber(self):
		"""bnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bnumber'):
			from .Bnumber import BnumberCls
			self._bnumber = BnumberCls(self._core, self._cmd_group)
		return self._bnumber

	@property
	def len(self):
		"""len commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_len'):
			from .Len import LenCls
			self._len = LenCls(self._core, self._cmd_group)
		return self._len

	@property
	def locked(self):
		"""locked commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_locked'):
			from .Locked import LockedCls
			self._locked = LockedCls(self._core, self._cmd_group)
		return self._locked

	@property
	def slOrder(self):
		"""slOrder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slOrder'):
			from .SlOrder import SlOrderCls
			self._slOrder = SlOrderCls(self._core, self._cmd_group)
		return self._slOrder

	def clone(self) -> 'BlockCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BlockCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
