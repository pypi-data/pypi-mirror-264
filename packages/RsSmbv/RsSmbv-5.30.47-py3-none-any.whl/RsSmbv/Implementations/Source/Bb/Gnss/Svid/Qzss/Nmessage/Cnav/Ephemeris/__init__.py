from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EphemerisCls:
	"""Ephemeris commands group definition. 50 total commands, 30 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ephemeris", core, parent)

	@property
	def adelta(self):
		"""adelta commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_adelta'):
			from .Adelta import AdeltaCls
			self._adelta = AdeltaCls(self._core, self._cmd_group)
		return self._adelta

	@property
	def adot(self):
		"""adot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_adot'):
			from .Adot import AdotCls
			self._adot = AdotCls(self._core, self._cmd_group)
		return self._adot

	@property
	def alert(self):
		"""alert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alert'):
			from .Alert import AlertCls
			self._alert = AlertCls(self._core, self._cmd_group)
		return self._alert

	@property
	def cic(self):
		"""cic commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cic'):
			from .Cic import CicCls
			self._cic = CicCls(self._core, self._cmd_group)
		return self._cic

	@property
	def cis(self):
		"""cis commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cis'):
			from .Cis import CisCls
			self._cis = CisCls(self._core, self._cmd_group)
		return self._cis

	@property
	def crc(self):
		"""crc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Crc import CrcCls
			self._crc = CrcCls(self._core, self._cmd_group)
		return self._crc

	@property
	def crs(self):
		"""crs commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_crs'):
			from .Crs import CrsCls
			self._crs = CrsCls(self._core, self._cmd_group)
		return self._crs

	@property
	def cuc(self):
		"""cuc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cuc'):
			from .Cuc import CucCls
			self._cuc = CucCls(self._core, self._cmd_group)
		return self._cuc

	@property
	def cus(self):
		"""cus commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cus'):
			from .Cus import CusCls
			self._cus = CusCls(self._core, self._cmd_group)
		return self._cus

	@property
	def dndot(self):
		"""dndot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_dndot'):
			from .Dndot import DndotCls
			self._dndot = DndotCls(self._core, self._cmd_group)
		return self._dndot

	@property
	def dodot(self):
		"""dodot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_dodot'):
			from .Dodot import DodotCls
			self._dodot = DodotCls(self._core, self._cmd_group)
		return self._dodot

	@property
	def eccentricity(self):
		"""eccentricity commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_eccentricity'):
			from .Eccentricity import EccentricityCls
			self._eccentricity = EccentricityCls(self._core, self._cmd_group)
		return self._eccentricity

	@property
	def idot(self):
		"""idot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_idot'):
			from .Idot import IdotCls
			self._idot = IdotCls(self._core, self._cmd_group)
		return self._idot

	@property
	def isFlag(self):
		"""isFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isFlag'):
			from .IsFlag import IsFlagCls
			self._isFlag = IsFlagCls(self._core, self._cmd_group)
		return self._isFlag

	@property
	def izero(self):
		"""izero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_izero'):
			from .Izero import IzeroCls
			self._izero = IzeroCls(self._core, self._cmd_group)
		return self._izero

	@property
	def l1Health(self):
		"""l1Health commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l1Health'):
			from .L1Health import L1HealthCls
			self._l1Health = L1HealthCls(self._core, self._cmd_group)
		return self._l1Health

	@property
	def l2Cphasing(self):
		"""l2Cphasing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l2Cphasing'):
			from .L2Cphasing import L2CphasingCls
			self._l2Cphasing = L2CphasingCls(self._core, self._cmd_group)
		return self._l2Cphasing

	@property
	def l2Health(self):
		"""l2Health commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l2Health'):
			from .L2Health import L2HealthCls
			self._l2Health = L2HealthCls(self._core, self._cmd_group)
		return self._l2Health

	@property
	def l5Health(self):
		"""l5Health commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l5Health'):
			from .L5Health import L5HealthCls
			self._l5Health = L5HealthCls(self._core, self._cmd_group)
		return self._l5Health

	@property
	def mzero(self):
		"""mzero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_mzero'):
			from .Mzero import MzeroCls
			self._mzero = MzeroCls(self._core, self._cmd_group)
		return self._mzero

	@property
	def ndelta(self):
		"""ndelta commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndelta'):
			from .Ndelta import NdeltaCls
			self._ndelta = NdeltaCls(self._core, self._cmd_group)
		return self._ndelta

	@property
	def ned0(self):
		"""ned0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ned0'):
			from .Ned0 import Ned0Cls
			self._ned0 = Ned0Cls(self._core, self._cmd_group)
		return self._ned0

	@property
	def ned1(self):
		"""ned1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ned1'):
			from .Ned1 import Ned1Cls
			self._ned1 = Ned1Cls(self._core, self._cmd_group)
		return self._ned1

	@property
	def ned2(self):
		"""ned2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ned2'):
			from .Ned2 import Ned2Cls
			self._ned2 = Ned2Cls(self._core, self._cmd_group)
		return self._ned2

	@property
	def odot(self):
		"""odot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_odot'):
			from .Odot import OdotCls
			self._odot = OdotCls(self._core, self._cmd_group)
		return self._odot

	@property
	def omega(self):
		"""omega commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_omega'):
			from .Omega import OmegaCls
			self._omega = OmegaCls(self._core, self._cmd_group)
		return self._omega

	@property
	def ozero(self):
		"""ozero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ozero'):
			from .Ozero import OzeroCls
			self._ozero = OzeroCls(self._core, self._cmd_group)
		return self._ozero

	@property
	def sqra(self):
		"""sqra commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sqra'):
			from .Sqra import SqraCls
			self._sqra = SqraCls(self._core, self._cmd_group)
		return self._sqra

	@property
	def toe(self):
		"""toe commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_toe'):
			from .Toe import ToeCls
			self._toe = ToeCls(self._core, self._cmd_group)
		return self._toe

	@property
	def ura(self):
		"""ura commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ura'):
			from .Ura import UraCls
			self._ura = UraCls(self._core, self._cmd_group)
		return self._ura

	def clone(self) -> 'EphemerisCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EphemerisCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
