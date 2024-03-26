from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrIndCls:
	"""SrInd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("srInd", core, parent)

	def set(self, srs_res_set_ind: int, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:USER<US(DIR0)>:BWPart<BWP(GR0)>:ALLoc<AL(USER0)>:CS:DCI<DCI(S2US0)>:SRINd \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.srInd.set(srs_res_set_ind = 1, cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines the bit pattern for the 'SRS Resource Set Indicator' DCI field. \n
			:param srs_res_set_ind: integer Range: 0 to 3
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Dci')
		"""
		param = Conversions.decimal_value_to_str(srs_res_set_ind)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CS:DCI{indexNull_cmd_val}:SRINd {param}')

	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default, indexNull=repcap.IndexNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CC(CH0)>:SUBF<SF(ST0)>:USER<US(DIR0)>:BWPart<BWP(GR0)>:ALLoc<AL(USER0)>:CS:DCI<DCI(S2US0)>:SRINd \n
		Snippet: value: int = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.srInd.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines the bit pattern for the 'SRS Resource Set Indicator' DCI field. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Dci')
			:return: srs_res_set_ind: No help available"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._cmd_group.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CS:DCI{indexNull_cmd_val}:SRINd?')
		return Conversions.str_to_int(response)
