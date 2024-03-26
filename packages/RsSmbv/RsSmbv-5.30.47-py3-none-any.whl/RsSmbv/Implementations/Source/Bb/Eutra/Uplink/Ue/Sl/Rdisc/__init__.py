from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RdiscCls:
	"""Rdisc commands group definition. 13 total commands, 13 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rdisc", core, parent)

	@property
	def cperiod(self):
		"""cperiod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cperiod'):
			from .Cperiod import CperiodCls
			self._cperiod = CperiodCls(self._core, self._cmd_group)
		return self._cperiod

	@property
	def n1Pdsch(self):
		"""n1Pdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n1Pdsch'):
			from .N1Pdsch import N1PdschCls
			self._n1Pdsch = N1PdschCls(self._core, self._cmd_group)
		return self._n1Pdsch

	@property
	def n2Pdsch(self):
		"""n2Pdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Pdsch'):
			from .N2Pdsch import N2PdschCls
			self._n2Pdsch = N2PdschCls(self._core, self._cmd_group)
		return self._n2Pdsch

	@property
	def n3Pdsch(self):
		"""n3Pdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n3Pdsch'):
			from .N3Pdsch import N3PdschCls
			self._n3Pdsch = N3PdschCls(self._core, self._cmd_group)
		return self._n3Pdsch

	@property
	def nrepetitions(self):
		"""nrepetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrepetitions'):
			from .Nrepetitions import NrepetitionsCls
			self._nrepetitions = NrepetitionsCls(self._core, self._cmd_group)
		return self._nrepetitions

	@property
	def nretrans(self):
		"""nretrans commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nretrans'):
			from .Nretrans import NretransCls
			self._nretrans = NretransCls(self._core, self._cmd_group)
		return self._nretrans

	@property
	def offsetInd(self):
		"""offsetInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offsetInd'):
			from .OffsetInd import OffsetIndCls
			self._offsetInd = OffsetIndCls(self._core, self._cmd_group)
		return self._offsetInd

	@property
	def prbNumber(self):
		"""prbNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbNumber'):
			from .PrbNumber import PrbNumberCls
			self._prbNumber = PrbNumberCls(self._core, self._cmd_group)
		return self._prbNumber

	@property
	def prbStart(self):
		"""prbStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbStart'):
			from .PrbStart import PrbStartCls
			self._prbStart = PrbStartCls(self._core, self._cmd_group)
		return self._prbStart

	@property
	def prend(self):
		"""prend commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prend'):
			from .Prend import PrendCls
			self._prend = PrendCls(self._core, self._cmd_group)
		return self._prend

	@property
	def prIndex(self):
		"""prIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prIndex'):
			from .PrIndex import PrIndexCls
			self._prIndex = PrIndexCls(self._core, self._cmd_group)
		return self._prIndex

	@property
	def sfbmp(self):
		"""sfbmp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfbmp'):
			from .Sfbmp import SfbmpCls
			self._sfbmp = SfbmpCls(self._core, self._cmd_group)
		return self._sfbmp

	@property
	def sfIndex(self):
		"""sfIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfIndex'):
			from .SfIndex import SfIndexCls
			self._sfIndex = SfIndexCls(self._core, self._cmd_group)
		return self._sfIndex

	def clone(self) -> 'RdiscCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RdiscCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
