from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UinfoCls:
	"""Uinfo commands group definition. 16 total commands, 16 Subgroups, 0 group commands
	Repeated Capability: TriggerFrameUser, default value after init: TriggerFrameUser.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uinfo", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_triggerFrameUser_get', 'repcap_triggerFrameUser_set', repcap.TriggerFrameUser.Nr1)

	def repcap_triggerFrameUser_set(self, triggerFrameUser: repcap.TriggerFrameUser) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TriggerFrameUser.Default
		Default value after init: TriggerFrameUser.Nr1"""
		self._cmd_group.set_repcap_enum_value(triggerFrameUser)

	def repcap_triggerFrameUser_get(self) -> repcap.TriggerFrameUser:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def aid(self):
		"""aid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aid'):
			from .Aid import AidCls
			self._aid = AidCls(self._core, self._cmd_group)
		return self._aid

	@property
	def codType(self):
		"""codType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_codType'):
			from .CodType import CodTypeCls
			self._codType = CodTypeCls(self._core, self._cmd_group)
		return self._codType

	@property
	def dcm(self):
		"""dcm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcm'):
			from .Dcm import DcmCls
			self._dcm = DcmCls(self._core, self._cmd_group)
		return self._dcm

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Mcs import McsCls
			self._mcs = McsCls(self._core, self._cmd_group)
		return self._mcs

	@property
	def ps160(self):
		"""ps160 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ps160'):
			from .Ps160 import Ps160Cls
			self._ps160 = Ps160Cls(self._core, self._cmd_group)
		return self._ps160

	@property
	def pvi(self):
		"""pvi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pvi'):
			from .Pvi import PviCls
			self._pvi = PviCls(self._core, self._cmd_group)
		return self._pvi

	@property
	def rsv(self):
		"""rsv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsv'):
			from .Rsv import RsvCls
			self._rsv = RsvCls(self._core, self._cmd_group)
		return self._rsv

	@property
	def ruAllocation(self):
		"""ruAllocation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruAllocation'):
			from .RuAllocation import RuAllocationCls
			self._ruAllocation = RuAllocationCls(self._core, self._cmd_group)
		return self._ruAllocation

	@property
	def sprFirst(self):
		"""sprFirst commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sprFirst'):
			from .SprFirst import SprFirstCls
			self._sprFirst = SprFirstCls(self._core, self._cmd_group)
		return self._sprFirst

	@property
	def sprSecond(self):
		"""sprSecond commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sprSecond'):
			from .SprSecond import SprSecondCls
			self._sprSecond = SprSecondCls(self._core, self._cmd_group)
		return self._sprSecond

	@property
	def ssAllocation(self):
		"""ssAllocation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssAllocation'):
			from .SsAllocation import SsAllocationCls
			self._ssAllocation = SsAllocationCls(self._core, self._cmd_group)
		return self._ssAllocation

	@property
	def tdUserInfo(self):
		"""tdUserInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdUserInfo'):
			from .TdUserInfo import TdUserInfoCls
			self._tdUserInfo = TdUserInfoCls(self._core, self._cmd_group)
		return self._tdUserInfo

	@property
	def trssi(self):
		"""trssi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trssi'):
			from .Trssi import TrssiCls
			self._trssi = TrssiCls(self._core, self._cmd_group)
		return self._trssi

	@property
	def ubExtension(self):
		"""ubExtension commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ubExtension'):
			from .UbExtension import UbExtensionCls
			self._ubExtension = UbExtensionCls(self._core, self._cmd_group)
		return self._ubExtension

	@property
	def udv(self):
		"""udv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_udv'):
			from .Udv import UdvCls
			self._udv = UdvCls(self._core, self._cmd_group)
		return self._udv

	@property
	def ureserved(self):
		"""ureserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ureserved'):
			from .Ureserved import UreservedCls
			self._ureserved = UreservedCls(self._core, self._cmd_group)
		return self._ureserved

	def clone(self) -> 'UinfoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UinfoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
