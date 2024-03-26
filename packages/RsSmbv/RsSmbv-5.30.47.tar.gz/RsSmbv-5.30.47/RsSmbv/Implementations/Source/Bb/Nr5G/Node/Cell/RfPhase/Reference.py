from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceCls:
	"""Reference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	def set(self, rf_phase_ref: enums.Output, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:RFPHase:REFerence \n
		Snippet: driver.source.bb.nr5G.node.cell.rfPhase.reference.set(rf_phase_ref = enums.Output.NONE, cellNull = repcap.CellNull.Default) \n
		Select the reference frequency for RF phase compensation. \n
			:param rf_phase_ref: RFA| RFB| NONE NONE Define the frequency manually with [:SOURcehw]:BB:NR5G:NODE:CELLcc:PCFReq. RFA | RFB Selects the frequency on path A or B as the reference frequency.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.enum_scalar_to_str(rf_phase_ref, enums.Output)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:RFPHase:REFerence {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.Output:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:RFPHase:REFerence \n
		Snippet: value: enums.Output = driver.source.bb.nr5G.node.cell.rfPhase.reference.get(cellNull = repcap.CellNull.Default) \n
		Select the reference frequency for RF phase compensation. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: rf_phase_ref: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:RFPHase:REFerence?')
		return Conversions.str_to_scalar_enum(response, enums.Output)
