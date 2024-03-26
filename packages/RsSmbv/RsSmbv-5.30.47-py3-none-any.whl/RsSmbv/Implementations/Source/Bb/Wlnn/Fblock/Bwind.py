from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwindCls:
	"""Bwind commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bwind", core, parent)

	def set(self, bw_type: enums.WlannFbPpdu320Mtype, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BWINd \n
		Snippet: driver.source.bb.wlnn.fblock.bwind.set(bw_type = enums.WlannFbPpdu320Mtype.T1_320, frameBlock = repcap.FrameBlock.Default) \n
		Sets the type of channelization of 320 MHz channels in the BW field of the U-SIG-1 field. The channelization affects two
		adjacent 160 MHz of a 320 MHz in the 6 GHz band. \n
			:param bw_type: T1_320| T2_320 T1_320 320MHz-1 channelization with channel center frequency numbers 31, 95 and 159. T2_320 320MHz-2 channelization with channel center frequency numbers 63, 127 and 191.
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.enum_scalar_to_str(bw_type, enums.WlannFbPpdu320Mtype)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BWINd {param}')

	# noinspection PyTypeChecker
	def get(self, frameBlock=repcap.FrameBlock.Default) -> enums.WlannFbPpdu320Mtype:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:BWINd \n
		Snippet: value: enums.WlannFbPpdu320Mtype = driver.source.bb.wlnn.fblock.bwind.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the type of channelization of 320 MHz channels in the BW field of the U-SIG-1 field. The channelization affects two
		adjacent 160 MHz of a 320 MHz in the 6 GHz band. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: bw_type: T1_320| T2_320 T1_320 320MHz-1 channelization with channel center frequency numbers 31, 95 and 159. T2_320 320MHz-2 channelization with channel center frequency numbers 63, 127 and 191."""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:BWINd?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPpdu320Mtype)
