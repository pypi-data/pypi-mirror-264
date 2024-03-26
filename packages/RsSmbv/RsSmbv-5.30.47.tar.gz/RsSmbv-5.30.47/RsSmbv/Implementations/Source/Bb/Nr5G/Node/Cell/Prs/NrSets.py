from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NrSetsCls:
	"""NrSets commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nrSets", core, parent)

	def set(self, num_res_set: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:PRS:NRSets \n
		Snippet: driver.source.bb.nr5G.node.cell.prs.nrSets.set(num_res_set = 1, cellNull = repcap.CellNull.Default) \n
		Sets the number of resource sets of the DL PRS frequency layer. \n
			:param num_res_set: integer Range: 1 to 8
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(num_res_set)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:PRS:NRSets {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:PRS:NRSets \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.prs.nrSets.get(cellNull = repcap.CellNull.Default) \n
		Sets the number of resource sets of the DL PRS frequency layer. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: num_res_set: integer Range: 1 to 8"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:PRS:NRSets?')
		return Conversions.str_to_int(response)
