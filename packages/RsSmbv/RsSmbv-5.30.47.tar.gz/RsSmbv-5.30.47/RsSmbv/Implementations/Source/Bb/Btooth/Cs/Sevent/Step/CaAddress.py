from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CaAddressCls:
	"""CaAddress commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("caAddress", core, parent)

	def set(self, access_address: List[str], bitcount: int, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CAADdress \n
		Snippet: driver.source.bb.btooth.cs.sevent.step.caAddress.set(access_address = ['rawAbc1', 'rawAbc2', 'rawAbc3'], bitcount = 1, channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param access_address: No help available
			:param bitcount: No help available
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('access_address', access_address, DataType.RawStringList, None), ArgSingle('bitcount', bitcount, DataType.Integer))
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CAADdress {param}'.rstrip())

	# noinspection PyTypeChecker
	class CaAddressStruct(StructBase):
		"""Response structure. Fields: \n
			- Access_Address: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Access_Address', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Access_Address: List[str] = None
			self.Bitcount: int = None

	def get(self, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> CaAddressStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:CAADdress \n
		Snippet: value: CaAddressStruct = driver.source.bb.btooth.cs.sevent.step.caAddress.get(channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		No command help available \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: structure: for return value, see the help for CaAddressStruct structure arguments."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:CAADdress?', self.__class__.CaAddressStruct())
