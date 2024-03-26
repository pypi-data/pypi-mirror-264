from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LengthCls:
	"""Length commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("length", core, parent)

	def set(self, length: enums.NumbersJ, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, listIndexNull=repcap.ListIndexNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:TDML<GRP0>:TD<USER0>:LENGth \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.tdml.td.length.set(length = enums.NumbersJ._10, userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, listIndexNull = repcap.ListIndexNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the number of consecutive OFDM symbols (L) the allocation in a time domain allocation list spans.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param length: 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12| 13| 14
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param listIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tdml')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')
		"""
		param = Conversions.enum_scalar_to_str(length, enums.NumbersJ)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		listIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(listIndexNull, repcap.ListIndexNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:TDML{listIndexNull_cmd_val}:TD{allocationNull_cmd_val}:LENGth {param}')

	# noinspection PyTypeChecker
	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, listIndexNull=repcap.ListIndexNull.Default, allocationNull=repcap.AllocationNull.Default) -> enums.NumbersJ:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:TDML<GRP0>:TD<USER0>:LENGth \n
		Snippet: value: enums.NumbersJ = driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.tdml.td.length.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, listIndexNull = repcap.ListIndexNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the number of consecutive OFDM symbols (L) the allocation in a time domain allocation list spans.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param listIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tdml')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')
			:return: length: 2| 3| 4| 5| 6| 7| 8| 9| 10| 11| 12| 13| 14"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		listIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(listIndexNull, repcap.ListIndexNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:TDML{listIndexNull_cmd_val}:TD{allocationNull_cmd_val}:LENGth?')
		return Conversions.str_to_scalar_enum(response, enums.NumbersJ)
