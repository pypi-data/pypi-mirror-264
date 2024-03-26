from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BsPeriodictyCls:
	"""BsPeriodicty commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bsPeriodicty", core, parent)

	def set(self, burst_set_per: enums.Nr5Gbsp, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:BSPeriodicty \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.bsPeriodicty.set(burst_set_per = enums.Nr5Gbsp.BS10, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Sets the burst set periodicity. \n
			:param burst_set_per: BS5| BS10| BS20| BS40| BS80| BS160| BS320| BS640
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(burst_set_per, enums.Nr5Gbsp)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:BSPeriodicty {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> enums.Nr5Gbsp:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:BSPeriodicty \n
		Snippet: value: enums.Nr5Gbsp = driver.source.bb.nr5G.node.cell.sspbch.bsPeriodicty.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Sets the burst set periodicity. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: burst_set_per: BS5| BS10| BS20| BS40| BS80| BS160| BS320| BS640"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:BSPeriodicty?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5Gbsp)
