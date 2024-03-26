from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class N2IdCls:
	"""N2Id commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("n2Id", core, parent)

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:N2ID \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.n2Id.get(cellNull = repcap.CellNull.Default) \n
		Queries the physical layer indicator group (NID(2) ). (Sidelink: NID,2SL) \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: carrier_n_2_id: integer Range: 0 to 2"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:N2ID?')
		return Conversions.str_to_int(response)
