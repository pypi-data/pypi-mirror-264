from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StepCls:
	"""Step commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("step", core, parent)

	def set(self, split_pat_scs_step: int, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:SPLT:SCS:STEP \n
		Snippet: driver.source.bb.ofdm.alloc.splt.scs.step.set(split_pat_scs_step = 1, allocationNull = repcap.AllocationNull.Default) \n
		Sets/queries the subcarrier spacing (SCS) step. Setting requires SCS sizes smaller than the set number of subcarriers of
		the selected allocation, see [:SOURce<hw>]:BB:OFDM:ALLoc<ch0>:SCNO. \n
			:param split_pat_scs_step: integer Range: 1 to 13107
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.decimal_value_to_str(split_pat_scs_step)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:SPLT:SCS:STEP {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:SPLT:SCS:STEP \n
		Snippet: value: int = driver.source.bb.ofdm.alloc.splt.scs.step.get(allocationNull = repcap.AllocationNull.Default) \n
		Sets/queries the subcarrier spacing (SCS) step. Setting requires SCS sizes smaller than the set number of subcarriers of
		the selected allocation, see [:SOURce<hw>]:BB:OFDM:ALLoc<ch0>:SCNO. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: split_pat_scs_step: integer Range: 1 to 13107"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:SPLT:SCS:STEP?')
		return Conversions.str_to_int(response)
