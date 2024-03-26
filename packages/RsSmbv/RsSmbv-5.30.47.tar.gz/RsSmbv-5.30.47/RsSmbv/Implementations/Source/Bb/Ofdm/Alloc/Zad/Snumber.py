from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SnumberCls:
	"""Snumber commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("snumber", core, parent)

	def set(self, seq_number: int, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:ZAD:SNUMber \n
		Snippet: driver.source.bb.ofdm.alloc.zad.snumber.set(seq_number = 1, allocationNull = repcap.AllocationNull.Default) \n
		Sets the sequence number within the Zadoff-Chu sequence. The maximum sequence number is the sequence length minus 1. \n
			:param seq_number: integer Range: 1 to 13106
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.decimal_value_to_str(seq_number)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:ZAD:SNUMber {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:ZAD:SNUMber \n
		Snippet: value: int = driver.source.bb.ofdm.alloc.zad.snumber.get(allocationNull = repcap.AllocationNull.Default) \n
		Sets the sequence number within the Zadoff-Chu sequence. The maximum sequence number is the sequence length minus 1. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: seq_number: integer Range: 1 to 13106"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:ZAD:SNUMber?')
		return Conversions.str_to_int(response)
