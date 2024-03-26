from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NapsCls:
	"""Naps commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("naps", core, parent)

	def set(self, num_aps: int, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:DUMRes:NAPS \n
		Snippet: driver.source.bb.nr5G.node.cell.dumRes.naps.set(num_aps = 1, cellNull = repcap.CellNull.Default) \n
		Selects the number of antenna ports that unused resource elements (dummy REs) are mapped to. \n
			:param num_aps: integer Range: 1 to 12
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.decimal_value_to_str(num_aps)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:DUMRes:NAPS {param}')

	def get(self, cellNull=repcap.CellNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:DUMRes:NAPS \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.dumRes.naps.get(cellNull = repcap.CellNull.Default) \n
		Selects the number of antenna ports that unused resource elements (dummy REs) are mapped to. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: num_aps: integer Range: 1 to 12"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:DUMRes:NAPS?')
		return Conversions.str_to_int(response)
