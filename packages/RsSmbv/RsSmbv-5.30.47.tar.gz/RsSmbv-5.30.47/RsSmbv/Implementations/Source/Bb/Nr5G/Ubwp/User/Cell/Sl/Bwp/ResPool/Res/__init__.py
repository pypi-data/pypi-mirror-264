from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ResCls:
	"""Res commands group definition. 19 total commands, 19 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("res", core, parent)

	@property
	def amcs(self):
		"""amcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amcs'):
			from .Amcs import AmcsCls
			self._amcs = AmcsCls(self._core, self._cmd_group)
		return self._amcs

	@property
	def bof1(self):
		"""bof1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bof1'):
			from .Bof1 import Bof1Cls
			self._bof1 = Bof1Cls(self._core, self._cmd_group)
		return self._bof1

	@property
	def bof2(self):
		"""bof2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bof2'):
			from .Bof2 import Bof2Cls
			self._bof2 = Bof2Cls(self._core, self._cmd_group)
		return self._bof2

	@property
	def bof3(self):
		"""bof3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bof3'):
			from .Bof3 import Bof3Cls
			self._bof3 = Bof3Cls(self._core, self._cmd_group)
		return self._bof3

	@property
	def bof4(self):
		"""bof4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bof4'):
			from .Bof4 import Bof4Cls
			self._bof4 = Bof4Cls(self._core, self._cmd_group)
		return self._bof4

	@property
	def indicator(self):
		"""indicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indicator'):
			from .Indicator import IndicatorCls
			self._indicator = IndicatorCls(self._core, self._cmd_group)
		return self._indicator

	@property
	def mnPres(self):
		"""mnPres commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mnPres'):
			from .MnPres import MnPresCls
			self._mnPres = MnPresCls(self._core, self._cmd_group)
		return self._mnPres

	@property
	def mreserve(self):
		"""mreserve commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mreserve'):
			from .Mreserve import MreserveCls
			self._mreserve = MreserveCls(self._core, self._cmd_group)
		return self._mreserve

	@property
	def mscTable(self):
		"""mscTable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mscTable'):
			from .MscTable import MscTableCls
			self._mscTable = MscTableCls(self._core, self._cmd_group)
		return self._mscTable

	@property
	def nprb(self):
		"""nprb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nprb'):
			from .Nprb import NprbCls
			self._nprb = NprbCls(self._core, self._cmd_group)
		return self._nprb

	@property
	def nsubChannels(self):
		"""nsubChannels commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsubChannels'):
			from .NsubChannels import NsubChannelsCls
			self._nsubChannels = NsubChannelsCls(self._core, self._cmd_group)
		return self._nsubChannels

	@property
	def pat2(self):
		"""pat2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pat2'):
			from .Pat2 import Pat2Cls
			self._pat2 = Pat2Cls(self._core, self._cmd_group)
		return self._pat2

	@property
	def pat3(self):
		"""pat3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pat3'):
			from .Pat3 import Pat3Cls
			self._pat3 = Pat3Cls(self._core, self._cmd_group)
		return self._pat3

	@property
	def pat4(self):
		"""pat4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pat4'):
			from .Pat4 import Pat4Cls
			self._pat4 = Pat4Cls(self._core, self._cmd_group)
		return self._pat4

	@property
	def repList(self):
		"""repList commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repList'):
			from .RepList import RepListCls
			self._repList = RepListCls(self._core, self._cmd_group)
		return self._repList

	@property
	def resBits(self):
		"""resBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resBits'):
			from .ResBits import ResBitsCls
			self._resBits = ResBitsCls(self._core, self._cmd_group)
		return self._resBits

	@property
	def scaling(self):
		"""scaling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scaling'):
			from .Scaling import ScalingCls
			self._scaling = ScalingCls(self._core, self._cmd_group)
		return self._scaling

	@property
	def schSize(self):
		"""schSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_schSize'):
			from .SchSize import SchSizeCls
			self._schSize = SchSizeCls(self._core, self._cmd_group)
		return self._schSize

	@property
	def strb(self):
		"""strb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_strb'):
			from .Strb import StrbCls
			self._strb = StrbCls(self._core, self._cmd_group)
		return self._strb

	def clone(self) -> 'ResCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ResCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
