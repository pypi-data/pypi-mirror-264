from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LselectedCls:
	"""Lselected commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lselected", core, parent)

	def set(self, sel_list: int, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:LSELected \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.lselected.set(sel_list = 1, userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default) \n
		Selects the allocation list you want to configure.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param sel_list: integer Range: 0 to 15
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
		"""
		param = Conversions.decimal_value_to_str(sel_list)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:LSELected {param}')

	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:LSELected \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.lselected.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default) \n
		Selects the allocation list you want to configure.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: sel_list: No help available"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:LSELected?')
		return Conversions.str_to_int(response)
