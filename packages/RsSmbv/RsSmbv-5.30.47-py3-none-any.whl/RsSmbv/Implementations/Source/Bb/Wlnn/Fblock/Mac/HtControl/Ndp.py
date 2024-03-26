from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NdpCls:
	"""Ndp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ndp", core, parent)

	def set(self, ndp: List[str], frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:NDP \n
		Snippet: driver.source.bb.wlnn.fblock.mac.htControl.ndp.set(ndp = ['rawAbc1', 'rawAbc2', 'rawAbc3'], frameBlock = repcap.FrameBlock.Default) \n
		Sets the value of the Null Data Packet (NDP) announcement. 0 = no NDP will follow 1 = NDP will follow \n
			:param ndp: integer
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.list_to_csv_str(ndp)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:NDP {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl:NDP \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.mac.htControl.ndp.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the value of the Null Data Packet (NDP) announcement. 0 = no NDP will follow 1 = NDP will follow \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ndp: integer"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl:NDP?')
		return Conversions.str_to_str_list(response)
