from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	def set(self, pbch_data_source: enums.DataSourceA, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:CCODing:DATA \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.ccoding.data.set(pbch_data_source = enums.DataSourceA.DLISt, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects the PBCH data source. \n
			:param pbch_data_source: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(pbch_data_source, enums.DataSourceA)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:CCODing:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> enums.DataSourceA:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:CCODing:DATA \n
		Snippet: value: enums.DataSourceA = driver.source.bb.nr5G.node.cell.sspbch.ccoding.data.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects the PBCH data source. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: pbch_data_source: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:CCODing:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceA)
