from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TdaNumCls:
	"""TdaNum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tdaNum", core, parent)

	def set(self, num_td_allocs: int, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, listIndexNull=repcap.ListIndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:TDML<GRP0>:TDANum \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.tdml.tdaNum.set(num_td_allocs = 1, userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, listIndexNull = repcap.ListIndexNull.Default) \n
		Defines the number of multi time domain allocations in the selected time domain allocation list.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param num_td_allocs: No help available
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param listIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tdml')
		"""
		param = Conversions.decimal_value_to_str(num_td_allocs)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		listIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(listIndexNull, repcap.ListIndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:TDML{listIndexNull_cmd_val}:TDANum {param}')

	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, listIndexNull=repcap.ListIndexNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:TDML<GRP0>:TDANum \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.tdml.tdaNum.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, listIndexNull = repcap.ListIndexNull.Default) \n
		Defines the number of multi time domain allocations in the selected time domain allocation list.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param listIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tdml')
			:return: num_td_allocs: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		listIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(listIndexNull, repcap.ListIndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:TDML{listIndexNull_cmd_val}:TDANum?')
		return Conversions.str_to_int(response)
