from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UmfbCls:
	"""Umfb commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("umfb", core, parent)

	def set(self, unsolicited_mfb: List[str], frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:UMFB \n
		Snippet: driver.source.bb.wlnn.fblock.mac.vhtControl.umfb.set(unsolicited_mfb = ['rawAbc1', 'rawAbc2', 'rawAbc3'], frameBlock = repcap.FrameBlock.Default) \n
		The command sets the Unsolicited MFB subfield. \n
			:param unsolicited_mfb: integer 0 if the MFB is a response to an MRQ. 1 if the MFB is not a response to an MRQ.
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.list_to_csv_str(unsolicited_mfb)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:UMFB {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:VHTControl:UMFB \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.mac.vhtControl.umfb.get(frameBlock = repcap.FrameBlock.Default) \n
		The command sets the Unsolicited MFB subfield. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: unsolicited_mfb: integer 0 if the MFB is a response to an MRQ. 1 if the MFB is not a response to an MRQ."""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:VHTControl:UMFB?')
		return Conversions.str_to_str_list(response)
