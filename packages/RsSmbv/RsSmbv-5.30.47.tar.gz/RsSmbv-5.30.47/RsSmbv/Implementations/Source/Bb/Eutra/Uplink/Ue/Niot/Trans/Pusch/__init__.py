from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschCls:
	"""Pusch commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pusch", core, parent)

	@property
	def esupport(self):
		"""esupport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_esupport'):
			from .Esupport import EsupportCls
			self._esupport = EsupportCls(self._core, self._cmd_group)
		return self._esupport

	@property
	def etbs(self):
		"""etbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_etbs'):
			from .Etbs import EtbsCls
			self._etbs = EtbsCls(self._core, self._cmd_group)
		return self._etbs

	@property
	def etrSize(self):
		"""etrSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_etrSize'):
			from .EtrSize import EtrSizeCls
			self._etrSize = EtrSizeCls(self._core, self._cmd_group)
		return self._etrSize

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .PhysBits import PhysBitsCls
			self._physBits = PhysBitsCls(self._core, self._cmd_group)
		return self._physBits

	@property
	def ruIndex(self):
		"""ruIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruIndex'):
			from .RuIndex import RuIndexCls
			self._ruIndex = RuIndexCls(self._core, self._cmd_group)
		return self._ruIndex

	@property
	def rvIndex(self):
		"""rvIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvIndex'):
			from .RvIndex import RvIndexCls
			self._rvIndex = RvIndexCls(self._core, self._cmd_group)
		return self._rvIndex

	@property
	def tbIndex(self):
		"""tbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbIndex'):
			from .TbIndex import TbIndexCls
			self._tbIndex = TbIndexCls(self._core, self._cmd_group)
		return self._tbIndex

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .TbSize import TbSizeCls
			self._tbSize = TbSizeCls(self._core, self._cmd_group)
		return self._tbSize

	def clone(self) -> 'PuschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PuschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
