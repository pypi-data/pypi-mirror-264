from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EphemerisCls:
	"""Ephemeris commands group definition. 36 total commands, 20 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ephemeris", core, parent)

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
	def eccentricity(self):
		"""eccentricity commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_eccentricity'):
			from .Eccentricity import EccentricityCls
			self._eccentricity = EccentricityCls(self._core, self._cmd_group)
		return self._eccentricity

	@property
	def health(self):
		"""health commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_health'):
			from .Health import HealthCls
			self._health = HealthCls(self._core, self._cmd_group)
		return self._health

	@property
	def idot(self):
		"""idot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_idot'):
			from .Idot import IdotCls
			self._idot = IdotCls(self._core, self._cmd_group)
		return self._idot

	@property
	def iodc(self):
		"""iodc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iodc'):
			from .Iodc import IodcCls
			self._iodc = IodcCls(self._core, self._cmd_group)
		return self._iodc

	@property
	def iode(self):
		"""iode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iode'):
			from .Iode import IodeCls
			self._iode = IodeCls(self._core, self._cmd_group)
		return self._iode

	@property
	def izero(self):
		"""izero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_izero'):
			from .Izero import IzeroCls
			self._izero = IzeroCls(self._core, self._cmd_group)
		return self._izero

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
