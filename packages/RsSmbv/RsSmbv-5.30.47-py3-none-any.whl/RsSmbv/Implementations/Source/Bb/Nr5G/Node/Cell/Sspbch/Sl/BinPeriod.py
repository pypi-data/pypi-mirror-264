from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BinPeriodCls:
	"""BinPeriod commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("binPeriod", core, parent)

	def set(self, blocks_in_period: enums.SsSpsbchBlocksAll, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:SL:BINPeriod \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.sl.binPeriod.set(blocks_in_period = enums.SsSpsbchBlocksAll.B1, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines the number of transmitted S-SS/PSBCH blocks.
			INTRO_CMD_HELP: Parameter values depend on: \n
			- Selected subcarrier spacing ([:SOURce<hw>]:BB:NR5G:NODE:CELL<cc>:SSPBch<ssb>:SCSPacing) . \n
			:param blocks_in_period: B1| B2| B4| B8| B16| B32| B64
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(blocks_in_period, enums.SsSpsbchBlocksAll)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:SL:BINPeriod {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> enums.SsSpsbchBlocksAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:SL:BINPeriod \n
		Snippet: value: enums.SsSpsbchBlocksAll = driver.source.bb.nr5G.node.cell.sspbch.sl.binPeriod.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines the number of transmitted S-SS/PSBCH blocks.
			INTRO_CMD_HELP: Parameter values depend on: \n
			- Selected subcarrier spacing ([:SOURce<hw>]:BB:NR5G:NODE:CELL<cc>:SSPBch<ssb>:SCSPacing) . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: blocks_in_period: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:SL:BINPeriod?')
		return Conversions.str_to_scalar_enum(response, enums.SsSpsbchBlocksAll)
