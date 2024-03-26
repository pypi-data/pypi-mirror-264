from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FcontrolCls:
	"""Fcontrol commands group definition. 12 total commands, 11 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fcontrol", core, parent)

	@property
	def fds(self):
		"""fds commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fds'):
			from .Fds import FdsCls
			self._fds = FdsCls(self._core, self._cmd_group)
		return self._fds

	@property
	def mdata(self):
		"""mdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mdata'):
			from .Mdata import MdataCls
			self._mdata = MdataCls(self._core, self._cmd_group)
		return self._mdata

	@property
	def mfragments(self):
		"""mfragments commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mfragments'):
			from .Mfragments import MfragmentsCls
			self._mfragments = MfragmentsCls(self._core, self._cmd_group)
		return self._mfragments

	@property
	def order(self):
		"""order commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_order'):
			from .Order import OrderCls
			self._order = OrderCls(self._core, self._cmd_group)
		return self._order

	@property
	def pmanagement(self):
		"""pmanagement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmanagement'):
			from .Pmanagement import PmanagementCls
			self._pmanagement = PmanagementCls(self._core, self._cmd_group)
		return self._pmanagement

	@property
	def pversion(self):
		"""pversion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pversion'):
			from .Pversion import PversionCls
			self._pversion = PversionCls(self._core, self._cmd_group)
		return self._pversion

	@property
	def retry(self):
		"""retry commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_retry'):
			from .Retry import RetryCls
			self._retry = RetryCls(self._core, self._cmd_group)
		return self._retry

	@property
	def subType(self):
		"""subType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subType'):
			from .SubType import SubTypeCls
			self._subType = SubTypeCls(self._core, self._cmd_group)
		return self._subType

	@property
	def tds(self):
		"""tds commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tds'):
			from .Tds import TdsCls
			self._tds = TdsCls(self._core, self._cmd_group)
		return self._tds

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def wep(self):
		"""wep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wep'):
			from .Wep import WepCls
			self._wep = WepCls(self._core, self._cmd_group)
		return self._wep

	def set(self, fcontrol: List[str], frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:FCONtrol \n
		Snippet: driver.source.bb.wlnn.fblock.user.mac.fcontrol.set(fcontrol = ['rawAbc1', 'rawAbc2', 'rawAbc3'], frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		The command enters the value of the frame control field. The frame control field has a length of 2 bytes (16 bits) and is
		used to define the protocol version, the frame type, and its function, etc.. As an alternative, the individual bits can
		be set with the following commands. \n
			:param fcontrol: integer Range: #H0000,16 to #HFFFF,16
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.list_to_csv_str(fcontrol)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:MAC:FCONtrol {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MAC:FCONtrol \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.user.mac.fcontrol.get(frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		The command enters the value of the frame control field. The frame control field has a length of 2 bytes (16 bits) and is
		used to define the protocol version, the frame type, and its function, etc.. As an alternative, the individual bits can
		be set with the following commands. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: fcontrol: integer Range: #H0000,16 to #HFFFF,16"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:MAC:FCONtrol?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'FcontrolCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FcontrolCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
