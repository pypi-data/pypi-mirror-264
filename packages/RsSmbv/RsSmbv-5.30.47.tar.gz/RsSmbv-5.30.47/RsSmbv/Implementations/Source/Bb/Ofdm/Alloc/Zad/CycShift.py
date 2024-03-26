from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CycShiftCls:
	"""CycShift commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cycShift", core, parent)

	def set(self, cyclic_shift: int, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:ZAD:CYCShift \n
		Snippet: driver.source.bb.ofdm.alloc.zad.cycShift.set(cyclic_shift = 1, allocationNull = repcap.AllocationNull.Default) \n
		Sets the cyclic shift of the Zadoff-Chu sequence. The maximum number of cyclic shifts is the sequence length minus 1. \n
			:param cyclic_shift: integer Range: 0 to 1023
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.decimal_value_to_str(cyclic_shift)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:ZAD:CYCShift {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:ZAD:CYCShift \n
		Snippet: value: int = driver.source.bb.ofdm.alloc.zad.cycShift.get(allocationNull = repcap.AllocationNull.Default) \n
		Sets the cyclic shift of the Zadoff-Chu sequence. The maximum number of cyclic shifts is the sequence length minus 1. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: cyclic_shift: integer Range: 0 to 1023"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:ZAD:CYCShift?')
		return Conversions.str_to_int(response)
