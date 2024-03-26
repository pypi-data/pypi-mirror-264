from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdelayCls:
	"""Fdelay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdelay", core, parent)

	def set(self, frame_delay: float, frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA:FDELay \n
		Snippet: driver.source.bb.wlnn.fblock.data.fdelay.set(frame_delay = 1.0, frameBlock = repcap.FrameBlock.Default) \n
		Shifts the frame in time by the specified frame delay value. \n
			:param frame_delay: float Range: 0 to 1000000
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.decimal_value_to_str(frame_delay)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:DATA:FDELay {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA:FDELay \n
		Snippet: value: float = driver.source.bb.wlnn.fblock.data.fdelay.get(frameBlock = repcap.FrameBlock.Default) \n
		Shifts the frame in time by the specified frame delay value. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: frame_delay: float Range: 0 to 1000000"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:DATA:FDELay?')
		return Conversions.str_to_float(response)
