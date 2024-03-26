from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NavCls:
	"""Nav commands group definition. 23 total commands, 12 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nav", core, parent)

	@property
	def almanac(self):
		"""almanac commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_almanac'):
			from .Almanac import AlmanacCls
			self._almanac = AlmanacCls(self._core, self._cmd_group)
		return self._almanac

	@property
	def ceCovariance(self):
		"""ceCovariance commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ceCovariance'):
			from .CeCovariance import CeCovarianceCls
			self._ceCovariance = CeCovarianceCls(self._core, self._cmd_group)
		return self._ceCovariance

	@property
	def dfactor(self):
		"""dfactor commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dfactor'):
			from .Dfactor import DfactorCls
			self._dfactor = DfactorCls(self._core, self._cmd_group)
		return self._dfactor

	@property
	def fcDegradation(self):
		"""fcDegradation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fcDegradation'):
			from .FcDegradation import FcDegradationCls
			self._fcDegradation = FcDegradationCls(self._core, self._cmd_group)
		return self._fcDegradation

	@property
	def fcorrection(self):
		"""fcorrection commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fcorrection'):
			from .Fcorrection import FcorrectionCls
			self._fcorrection = FcorrectionCls(self._core, self._cmd_group)
		return self._fcorrection

	@property
	def igrid(self):
		"""igrid commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_igrid'):
			from .Igrid import IgridCls
			self._igrid = IgridCls(self._core, self._cmd_group)
		return self._igrid

	@property
	def ltCorrection(self):
		"""ltCorrection commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ltCorrection'):
			from .LtCorrection import LtCorrectionCls
			self._ltCorrection = LtCorrectionCls(self._core, self._cmd_group)
		return self._ltCorrection

	@property
	def prNoise(self):
		"""prNoise commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_prNoise'):
			from .PrNoise import PrNoiseCls
			self._prNoise = PrNoiseCls(self._core, self._cmd_group)
		return self._prNoise

	@property
	def prnMask(self):
		"""prnMask commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_prnMask'):
			from .PrnMask import PrnMaskCls
			self._prnMask = PrnMaskCls(self._core, self._cmd_group)
		return self._prnMask

	@property
	def rinex(self):
		"""rinex commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rinex'):
			from .Rinex import RinexCls
			self._rinex = RinexCls(self._core, self._cmd_group)
		return self._rinex

	@property
	def service(self):
		"""service commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_service'):
			from .Service import ServiceCls
			self._service = ServiceCls(self._core, self._cmd_group)
		return self._service

	@property
	def utcOffset(self):
		"""utcOffset commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_utcOffset'):
			from .UtcOffset import UtcOffsetCls
			self._utcOffset = UtcOffsetCls(self._core, self._cmd_group)
		return self._utcOffset

	def clone(self) -> 'NavCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NavCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
