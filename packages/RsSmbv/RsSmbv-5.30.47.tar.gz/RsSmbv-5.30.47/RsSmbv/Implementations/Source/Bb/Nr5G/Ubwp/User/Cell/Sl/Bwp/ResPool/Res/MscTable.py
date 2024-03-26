from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MscTableCls:
	"""MscTable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mscTable", core, parent)

	def set(self, mcs_table: enums.McsTable, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:SL:BWP<BWP(DIR0)>:RESPool:RES:MSCTable \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.sl.bwp.resPool.res.mscTable.set(mcs_table = enums.McsTable.QAM256, userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default) \n
		Selects the modulation (MCS table) for the resource pool. \n
			:param mcs_table: QAM64| QAM256| QAM64LSE
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
		"""
		param = Conversions.enum_scalar_to_str(mcs_table, enums.McsTable)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:SL:BWP{bwPartNull_cmd_val}:RESPool:RES:MSCTable {param}')

	# noinspection PyTypeChecker
	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default) -> enums.McsTable:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:SL:BWP<BWP(DIR0)>:RESPool:RES:MSCTable \n
		Snippet: value: enums.McsTable = driver.source.bb.nr5G.ubwp.user.cell.sl.bwp.resPool.res.mscTable.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default) \n
		Selects the modulation (MCS table) for the resource pool. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: mcs_table: QAM64| QAM256| QAM64LSE"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:SL:BWP{bwPartNull_cmd_val}:RESPool:RES:MSCTable?')
		return Conversions.str_to_scalar_enum(response, enums.McsTable)
