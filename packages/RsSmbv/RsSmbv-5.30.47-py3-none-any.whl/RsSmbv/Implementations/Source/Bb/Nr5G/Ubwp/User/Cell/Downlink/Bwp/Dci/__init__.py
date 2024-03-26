from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DciCls:
	"""Dci commands group definition. 17 total commands, 17 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dci", core, parent)

	@property
	def dai2(self):
		"""dai2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dai2'):
			from .Dai2 import Dai2Cls
			self._dai2 = Dai2Cls(self._core, self._cmd_group)
		return self._dai2

	@property
	def dai3(self):
		"""dai3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dai3'):
			from .Dai3 import Dai3Cls
			self._dai3 = Dai3Cls(self._core, self._cmd_group)
		return self._dai3

	@property
	def ds42(self):
		"""ds42 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ds42'):
			from .Ds42 import Ds42Cls
			self._ds42 = Ds42Cls(self._core, self._cmd_group)
		return self._ds42

	@property
	def haEnabler(self):
		"""haEnabler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_haEnabler'):
			from .HaEnabler import HaEnablerCls
			self._haEnabler = HaEnablerCls(self._core, self._cmd_group)
		return self._haEnabler

	@property
	def hartInd(self):
		"""hartInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hartInd'):
			from .HartInd import HartIndCls
			self._hartInd = HartIndCls(self._core, self._cmd_group)
		return self._hartInd

	@property
	def ltechan(self):
		"""ltechan commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ltechan'):
			from .Ltechan import LtechanCls
			self._ltechan = LtechanCls(self._core, self._cmd_group)
		return self._ltechan

	@property
	def pnpPei(self):
		"""pnpPei commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pnpPei'):
			from .PnpPei import PnpPeiCls
			self._pnpPei = PnpPeiCls(self._core, self._cmd_group)
		return self._pnpPei

	@property
	def prc2(self):
		"""prc2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prc2'):
			from .Prc2 import Prc2Cls
			self._prc2 = Prc2Cls(self._core, self._cmd_group)
		return self._prc2

	@property
	def prIndicator(self):
		"""prIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prIndicator'):
			from .PrIndicator import PrIndicatorCls
			self._prIndicator = PrIndicatorCls(self._core, self._cmd_group)
		return self._prIndicator

	@property
	def ps27(self):
		"""ps27 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ps27'):
			from .Ps27 import Ps27Cls
			self._ps27 = Ps27Cls(self._core, self._cmd_group)
		return self._ps27

	@property
	def psscDyn(self):
		"""psscDyn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psscDyn'):
			from .PsscDyn import PsscDynCls
			self._psscDyn = PsscDynCls(self._core, self._cmd_group)
		return self._psscDyn

	@property
	def ptpSlots(self):
		"""ptpSlots commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptpSlots'):
			from .PtpSlots import PtpSlotsCls
			self._ptpSlots = PtpSlotsCls(self._core, self._cmd_group)
		return self._ptpSlots

	@property
	def sgpo(self):
		"""sgpo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgpo'):
			from .Sgpo import SgpoCls
			self._sgpo = SgpoCls(self._core, self._cmd_group)
		return self._sgpo

	@property
	def soin(self):
		"""soin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soin'):
			from .Soin import SoinCls
			self._soin = SoinCls(self._core, self._cmd_group)
		return self._soin

	@property
	def sri2(self):
		"""sri2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sri2'):
			from .Sri2 import Sri2Cls
			self._sri2 = Sri2Cls(self._core, self._cmd_group)
		return self._sri2

	@property
	def srInd(self):
		"""srInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srInd'):
			from .SrInd import SrIndCls
			self._srInd = SrIndCls(self._core, self._cmd_group)
		return self._srInd

	@property
	def taInd(self):
		"""taInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taInd'):
			from .TaInd import TaIndCls
			self._taInd = TaIndCls(self._core, self._cmd_group)
		return self._taInd

	def clone(self) -> 'DciCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DciCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
