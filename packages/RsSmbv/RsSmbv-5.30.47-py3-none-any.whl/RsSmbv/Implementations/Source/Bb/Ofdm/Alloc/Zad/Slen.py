from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlenCls:
	"""Slen commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slen", core, parent)

	def set(self, seq_length: int, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:ZAD:SLEN \n
		Snippet: driver.source.bb.ofdm.alloc.zad.slen.set(seq_length = 1, allocationNull = repcap.AllocationNull.Default) \n
		Sets the sequence length of the Zadoff-Chu sequence. \n
			:param seq_length: integer Range: 2 to 13107
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.decimal_value_to_str(seq_length)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:ZAD:SLEN {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:ZAD:SLEN \n
		Snippet: value: int = driver.source.bb.ofdm.alloc.zad.slen.get(allocationNull = repcap.AllocationNull.Default) \n
		Sets the sequence length of the Zadoff-Chu sequence. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: seq_length: integer Range: 2 to 13107"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:ZAD:SLEN?')
		return Conversions.str_to_int(response)
