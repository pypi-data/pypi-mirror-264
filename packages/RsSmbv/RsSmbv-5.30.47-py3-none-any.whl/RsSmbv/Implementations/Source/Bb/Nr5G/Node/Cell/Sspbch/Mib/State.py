from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, ssp_bch_mib_state: bool, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:STATe \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.mib.state.set(ssp_bch_mib_state = False, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines how the MIB is defined. \n
			:param ssp_bch_mib_state: 1| ON| 0| OFF 1|ON A faster way to define the MIB. You can define if channel coding is used or not and select an arbitrary data source; further settings are not required. 0|OFF Allows you to configure the MIB content according to .
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.bool_to_str(ssp_bch_mib_state)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:STATe {param}')

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:STATe \n
		Snippet: value: bool = driver.source.bb.nr5G.node.cell.sspbch.mib.state.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines how the MIB is defined. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: ssp_bch_mib_state: 1| ON| 0| OFF 1|ON A faster way to define the MIB. You can define if channel coding is used or not and select an arbitrary data source; further settings are not required. 0|OFF Allows you to configure the MIB content according to ."""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:STATe?')
		return Conversions.str_to_bool(response)
