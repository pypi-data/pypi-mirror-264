from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MappingCls:
	"""Mapping commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mapping", core, parent)

	def set(self, mapping_type: enums.MappingType, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, listIndexNull=repcap.ListIndexNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:TDML<GRP0>:TD<USER0>:MAPPing \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.tdml.td.mapping.set(mapping_type = enums.MappingType.A, userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, listIndexNull = repcap.ListIndexNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the DMRS-mapping type for an allocation in a time domain allocation list.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param mapping_type: A| B
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param listIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tdml')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')
		"""
		param = Conversions.enum_scalar_to_str(mapping_type, enums.MappingType)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		listIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(listIndexNull, repcap.ListIndexNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:TDML{listIndexNull_cmd_val}:TD{allocationNull_cmd_val}:MAPPing {param}')

	# noinspection PyTypeChecker
	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, listIndexNull=repcap.ListIndexNull.Default, allocationNull=repcap.AllocationNull.Default) -> enums.MappingType:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:DL:BWP<BWP(DIR0)>:PDSCh:TDML<GRP0>:TD<USER0>:MAPPing \n
		Snippet: value: enums.MappingType = driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.pdsch.tdml.td.mapping.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, listIndexNull = repcap.ListIndexNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the DMRS-mapping type for an allocation in a time domain allocation list.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:PDSCh:TDALists > 1 \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param listIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tdml')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Td')
			:return: mapping_type: A| B"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		listIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(listIndexNull, repcap.ListIndexNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:PDSCh:TDML{listIndexNull_cmd_val}:TD{allocationNull_cmd_val}:MAPPing?')
		return Conversions.str_to_scalar_enum(response, enums.MappingType)
