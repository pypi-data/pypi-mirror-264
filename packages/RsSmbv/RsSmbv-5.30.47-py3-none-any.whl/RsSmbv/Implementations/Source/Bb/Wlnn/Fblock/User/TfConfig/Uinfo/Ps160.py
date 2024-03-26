from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ps160Cls:
	"""Ps160 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ps160", core, parent)

	def set(self, ps_160: List[str], frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default, triggerFrameUser=repcap.TriggerFrameUser.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:UINFo<ST0>:PS160 \n
		Snippet: driver.source.bb.wlnn.fblock.user.tfConfig.uinfo.ps160.set(ps_160 = ['rawAbc1', 'rawAbc2', 'rawAbc3'], frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default, triggerFrameUser = repcap.TriggerFrameUser.Default) \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the following
		command: [:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param ps_160: 3 bits
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param triggerFrameUser: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Uinfo')
		"""
		param = Conversions.list_to_csv_str(ps_160)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		triggerFrameUser_cmd_val = self._cmd_group.get_repcap_cmd_value(triggerFrameUser, repcap.TriggerFrameUser)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:UINFo{triggerFrameUser_cmd_val}:PS160 {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default, triggerFrameUser=repcap.TriggerFrameUser.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:UINFo<ST0>:PS160 \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.user.tfConfig.uinfo.ps160.get(frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default, triggerFrameUser = repcap.TriggerFrameUser.Default) \n
		Sets the value bits of the user info field. You can configure the user info for up to 37 users with the following
		command: [:SOURce<hw>]:BB:WLNN:FBLock<ch>[:USER<di>]:TFConfig:NUINfo. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param triggerFrameUser: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Uinfo')
			:return: ps_160: No help available"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		triggerFrameUser_cmd_val = self._cmd_group.get_repcap_cmd_value(triggerFrameUser, repcap.TriggerFrameUser)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:UINFo{triggerFrameUser_cmd_val}:PS160?')
		return Conversions.str_to_str_list(response)
