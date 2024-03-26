from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpTimeCls:
	"""TpTime commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpTime", core, parent)

	def set(self, trig_proc_time: enums.WlannFbTrigFrmMinTrigProcTime, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:TPTime \n
		Snippet: driver.source.bb.wlnn.fblock.user.tfConfig.tpTime.set(trig_proc_time = enums.WlannFbTrigFrmMinTrigProcTime.TPT0, frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		Sets minimum time to process the trigger frame in microseconds. \n
			:param trig_proc_time: TPT0| TPT8| TPT16 TPT0|TPT8|TPT16 0/8/16 us
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(trig_proc_time, enums.WlannFbTrigFrmMinTrigProcTime)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:TPTime {param}')

	# noinspection PyTypeChecker
	def get(self, frameBlock=repcap.FrameBlock.Default, userIx=repcap.UserIx.Default) -> enums.WlannFbTrigFrmMinTrigProcTime:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:TFConfig:TPTime \n
		Snippet: value: enums.WlannFbTrigFrmMinTrigProcTime = driver.source.bb.wlnn.fblock.user.tfConfig.tpTime.get(frameBlock = repcap.FrameBlock.Default, userIx = repcap.UserIx.Default) \n
		Sets minimum time to process the trigger frame in microseconds. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: trig_proc_time: TPT0| TPT8| TPT16 TPT0|TPT8|TPT16 0/8/16 us"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:USER{userIx_cmd_val}:TFConfig:TPTime?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbTrigFrmMinTrigProcTime)
