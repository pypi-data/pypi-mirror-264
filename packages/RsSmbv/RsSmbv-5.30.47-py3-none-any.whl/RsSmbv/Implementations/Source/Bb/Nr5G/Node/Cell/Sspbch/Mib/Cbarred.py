from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CbarredCls:
	"""Cbarred commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cbarred", core, parent)

	def set(self, ssp_bch_cell_barre: enums.CellBarring, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:CBARred \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.mib.cbarred.set(ssp_bch_cell_barre = enums.CellBarring.BARR, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Cell barring is system information that indicates if UEs can camp on the particular cell NBAR or not BARR. \n
			:param ssp_bch_cell_barre: BARR| NBAR
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(ssp_bch_cell_barre, enums.CellBarring)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:CBARred {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> enums.CellBarring:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:CBARred \n
		Snippet: value: enums.CellBarring = driver.source.bb.nr5G.node.cell.sspbch.mib.cbarred.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Cell barring is system information that indicates if UEs can camp on the particular cell NBAR or not BARR. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: ssp_bch_cell_barre: BARR| NBAR"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:CBARred?')
		return Conversions.str_to_scalar_enum(response, enums.CellBarring)
