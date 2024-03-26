from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EphemerisCls:
	"""Ephemeris commands group definition. 29 total commands, 19 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ephemeris", core, parent)

	@property
	def aoep(self):
		"""aoep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aoep'):
			from .Aoep import AoepCls
			self._aoep = AoepCls(self._core, self._cmd_group)
		return self._aoep

	@property
	def cfm(self):
		"""cfm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfm'):
			from .Cfm import CfmCls
			self._cfm = CfmCls(self._core, self._cmd_group)
		return self._cfm

	@property
	def health(self):
		"""health commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_health'):
			from .Health import HealthCls
			self._health = HealthCls(self._core, self._cmd_group)
		return self._health

	@property
	def p(self):
		"""p commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_p'):
			from .P import PCls
			self._p = PCls(self._core, self._cmd_group)
		return self._p

	@property
	def seType(self):
		"""seType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seType'):
			from .SeType import SeTypeCls
			self._seType = SeTypeCls(self._core, self._cmd_group)
		return self._seType

	@property
	def talignment(self):
		"""talignment commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_talignment'):
			from .Talignment import TalignmentCls
			self._talignment = TalignmentCls(self._core, self._cmd_group)
		return self._talignment

	@property
	def tindex(self):
		"""tindex commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tindex'):
			from .Tindex import TindexCls
			self._tindex = TindexCls(self._core, self._cmd_group)
		return self._tindex

	@property
	def tinterval(self):
		"""tinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tinterval'):
			from .Tinterval import TintervalCls
			self._tinterval = TintervalCls(self._core, self._cmd_group)
		return self._tinterval

	@property
	def toe(self):
		"""toe commands group. 0 Sub-classes, 1 commands."""
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

	@property
	def xddn(self):
		"""xddn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_xddn'):
			from .Xddn import XddnCls
			self._xddn = XddnCls(self._core, self._cmd_group)
		return self._xddn

	@property
	def xdn(self):
		"""xdn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_xdn'):
			from .Xdn import XdnCls
			self._xdn = XdnCls(self._core, self._cmd_group)
		return self._xdn

	@property
	def xn(self):
		"""xn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_xn'):
			from .Xn import XnCls
			self._xn = XnCls(self._core, self._cmd_group)
		return self._xn

	@property
	def yddn(self):
		"""yddn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_yddn'):
			from .Yddn import YddnCls
			self._yddn = YddnCls(self._core, self._cmd_group)
		return self._yddn

	@property
	def ydn(self):
		"""ydn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ydn'):
			from .Ydn import YdnCls
			self._ydn = YdnCls(self._core, self._cmd_group)
		return self._ydn

	@property
	def yn(self):
		"""yn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_yn'):
			from .Yn import YnCls
			self._yn = YnCls(self._core, self._cmd_group)
		return self._yn

	@property
	def zddn(self):
		"""zddn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_zddn'):
			from .Zddn import ZddnCls
			self._zddn = ZddnCls(self._core, self._cmd_group)
		return self._zddn

	@property
	def zdn(self):
		"""zdn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_zdn'):
			from .Zdn import ZdnCls
			self._zdn = ZdnCls(self._core, self._cmd_group)
		return self._zdn

	@property
	def zn(self):
		"""zn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_zn'):
			from .Zn import ZnCls
			self._zn = ZnCls(self._core, self._cmd_group)
		return self._zn

	def clone(self) -> 'EphemerisCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EphemerisCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
