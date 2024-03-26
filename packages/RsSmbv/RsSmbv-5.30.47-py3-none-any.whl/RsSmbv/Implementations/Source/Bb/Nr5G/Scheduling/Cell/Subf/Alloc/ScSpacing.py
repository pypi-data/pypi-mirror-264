from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScSpacingCls:
	"""ScSpacing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scSpacing", core, parent)

	def set(self, alloc_numerology: enums.QucjSettingsScsAll, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:ALLoc<AL(DIR0)>:SCSPacing \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.alloc.scSpacing.set(alloc_numerology = enums.QucjSettingsScsAll.N120, cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Defines the subcarrier spacing for the selected allocation.
			INTRO_CMD_HELP: To define the subcarrier spacings for the complete bandwidth part and thus its user allocations in the various link directions, use the following commands: \n
			- Downlink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:SCSPacing
			- Uplink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:UL:BWP<bwp>:SCSPacing
			- Sidelink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:SL:BWP<bwp>:SCSPacing \n
			:param alloc_numerology: SCS15| SCS30| SCS60| SCS120| SCS240| N15| N30| N60| N120| N240| SCS480| SCS960 Available subcarrier spacings depend on the channel type.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
		"""
		param = Conversions.enum_scalar_to_str(alloc_numerology, enums.QucjSettingsScsAll)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:SCSPacing {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> enums.QucjSettingsScsAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:ALLoc<AL(DIR0)>:SCSPacing \n
		Snippet: value: enums.QucjSettingsScsAll = driver.source.bb.nr5G.scheduling.cell.subf.alloc.scSpacing.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Defines the subcarrier spacing for the selected allocation.
			INTRO_CMD_HELP: To define the subcarrier spacings for the complete bandwidth part and thus its user allocations in the various link directions, use the following commands: \n
			- Downlink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:DL:BWP<bwp>:SCSPacing
			- Uplink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:UL:BWP<bwp>:SCSPacing
			- Sidelink: [:SOURce<hw>]:BB:NR5G:UBWP:USER<us>:CELL<cc>:SL:BWP<bwp>:SCSPacing \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: alloc_numerology: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.QucjSettingsScsAll)
