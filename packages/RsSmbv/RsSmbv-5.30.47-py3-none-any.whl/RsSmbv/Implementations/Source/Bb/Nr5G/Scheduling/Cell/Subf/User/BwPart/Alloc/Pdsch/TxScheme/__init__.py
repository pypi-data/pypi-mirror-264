from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxSchemeCls:
	"""TxScheme commands group definition. 12 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("txScheme", core, parent)

	@property
	def apcsirs(self):
		"""apcsirs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apcsirs'):
			from .Apcsirs import ApcsirsCls
			self._apcsirs = ApcsirsCls(self._core, self._cmd_group)
		return self._apcsirs

	@property
	def cbmd(self):
		"""cbmd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbmd'):
			from .Cbmd import CbmdCls
			self._cbmd = CbmdCls(self._core, self._cmd_group)
		return self._cbmd

	@property
	def cbType(self):
		"""cbType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbType'):
			from .CbType import CbTypeCls
			self._cbType = CbTypeCls(self._core, self._cmd_group)
		return self._cbType

	@property
	def cdmData(self):
		"""cdmData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdmData'):
			from .CdmData import CdmDataCls
			self._cdmData = CdmDataCls(self._core, self._cmd_group)
		return self._cdmData

	@property
	def intervp(self):
		"""intervp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_intervp'):
			from .Intervp import IntervpCls
			self._intervp = IntervpCls(self._core, self._cmd_group)
		return self._intervp

	@property
	def nlayers(self):
		"""nlayers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nlayers'):
			from .Nlayers import NlayersCls
			self._nlayers = NlayersCls(self._core, self._cmd_group)
		return self._nlayers

	@property
	def pcn1(self):
		"""pcn1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcn1'):
			from .Pcn1 import Pcn1Cls
			self._pcn1 = Pcn1Cls(self._core, self._cmd_group)
		return self._pcn1

	@property
	def pcn2(self):
		"""pcn2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcn2'):
			from .Pcn2 import Pcn2Cls
			self._pcn2 = Pcn2Cls(self._core, self._cmd_group)
		return self._pcn2

	@property
	def spcb(self):
		"""spcb commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spcb'):
			from .Spcb import SpcbCls
			self._spcb = SpcbCls(self._core, self._cmd_group)
		return self._spcb

	def clone(self) -> 'TxSchemeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TxSchemeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
