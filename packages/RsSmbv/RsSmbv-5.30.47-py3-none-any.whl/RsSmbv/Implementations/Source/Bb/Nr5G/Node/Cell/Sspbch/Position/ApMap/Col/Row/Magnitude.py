from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MagnitudeCls:
	"""Magnitude commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("magnitude", core, parent)

	def set(self, ssp_bch_ap_magn: float, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default, antennaPortNull=repcap.AntennaPortNull.Default, columnNull=repcap.ColumnNull.Default, rowNull=repcap.RowNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:POSition:APMap<DIR0>:COL<APC(GR0)>:ROW<APR(USER0)>:MAGNitude \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.position.apMap.col.row.magnitude.set(ssp_bch_ap_magn = 1.0, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default, antennaPortNull = repcap.AntennaPortNull.Default, columnNull = repcap.ColumnNull.Default, rowNull = repcap.RowNull.Default) \n
		Defines the mapping of the antenna ports to the physical antennas for the SS/PBCH pattern if cylindrical mapping
		coordinates are used. \n
			:param ssp_bch_ap_magn: No help available
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:param antennaPortNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApMap')
			:param columnNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
		"""
		param = Conversions.decimal_value_to_str(ssp_bch_ap_magn)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		antennaPortNull_cmd_val = self._cmd_group.get_repcap_cmd_value(antennaPortNull, repcap.AntennaPortNull)
		columnNull_cmd_val = self._cmd_group.get_repcap_cmd_value(columnNull, repcap.ColumnNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:POSition:APMap{antennaPortNull_cmd_val}:COL{columnNull_cmd_val}:ROW{rowNull_cmd_val}:MAGNitude {param}')

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default, antennaPortNull=repcap.AntennaPortNull.Default, columnNull=repcap.ColumnNull.Default, rowNull=repcap.RowNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:POSition:APMap<DIR0>:COL<APC(GR0)>:ROW<APR(USER0)>:MAGNitude \n
		Snippet: value: float = driver.source.bb.nr5G.node.cell.sspbch.position.apMap.col.row.magnitude.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default, antennaPortNull = repcap.AntennaPortNull.Default, columnNull = repcap.ColumnNull.Default, rowNull = repcap.RowNull.Default) \n
		Defines the mapping of the antenna ports to the physical antennas for the SS/PBCH pattern if cylindrical mapping
		coordinates are used. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:param antennaPortNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ApMap')
			:param columnNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Col')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: ssp_bch_ap_magn: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		antennaPortNull_cmd_val = self._cmd_group.get_repcap_cmd_value(antennaPortNull, repcap.AntennaPortNull)
		columnNull_cmd_val = self._cmd_group.get_repcap_cmd_value(columnNull, repcap.ColumnNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:POSition:APMap{antennaPortNull_cmd_val}:COL{columnNull_cmd_val}:ROW{rowNull_cmd_val}:MAGNitude?')
		return Conversions.str_to_float(response)
