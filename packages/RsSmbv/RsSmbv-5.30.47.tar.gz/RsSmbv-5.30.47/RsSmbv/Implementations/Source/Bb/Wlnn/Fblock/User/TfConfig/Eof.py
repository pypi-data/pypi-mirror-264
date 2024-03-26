from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EofCls:
	"""Eof commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eof", core, parent)

	def set(self, mpdu_eof: enums.WlannFbMpduEof, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:EOF \n
		Snippet: driver.source.bb.wlnn.fblock.user.tfConfig.eof.set(mpdu_eof = enums.WlannFbMpduEof.E0, frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		Selects the end of frame (EOF) tag. Tagged/untagged indication is set in the 1-bit EOF/Tag field of an MPDU. \n
			:param mpdu_eof: E0| E1 E0 End of frame is untagged. E1 End of frame is tagged.
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(mpdu_eof, enums.WlannFbMpduEof)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:EOF {param}')

	# noinspection PyTypeChecker
	def get(self, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> enums.WlannFbMpduEof:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:EOF \n
		Snippet: value: enums.WlannFbMpduEof = driver.source.bb.wlnn.fblock.user.tfConfig.eof.get(frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		Selects the end of frame (EOF) tag. Tagged/untagged indication is set in the 1-bit EOF/Tag field of an MPDU. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: mpdu_eof: E0| E1 E0 End of frame is untagged. E1 End of frame is tagged."""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:EOF?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbMpduEof)
