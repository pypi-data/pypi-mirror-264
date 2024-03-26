from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MoorCls:
	"""Moor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("moor", core, parent)

	def set(self, mod_order: int, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:MOOR \n
		Snippet: driver.source.bb.ofdm.alloc.moor.set(mod_order = 1, allocationNull = repcap.AllocationNull.Default) \n
		Sets/queries the modulation order of the allocation. Setting requires custom constellation modulation,
		see [:SOURce<hw>]:BB:OFDM:ALLoc<ch0>:MODulation. \n
			:param mod_order: integer Range: 2 to 4096
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.decimal_value_to_str(mod_order)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:MOOR {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:MOOR \n
		Snippet: value: int = driver.source.bb.ofdm.alloc.moor.get(allocationNull = repcap.AllocationNull.Default) \n
		Sets/queries the modulation order of the allocation. Setting requires custom constellation modulation,
		see [:SOURce<hw>]:BB:OFDM:ALLoc<ch0>:MODulation. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: mod_order: integer Range: 2 to 4096"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:MOOR?')
		return Conversions.str_to_int(response)
