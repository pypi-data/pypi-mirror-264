from .................Internal.Core import Core
from .................Internal.CommandsGroup import CommandsGroup
from .................Internal import Conversions
from ................. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RealCls:
	"""Real commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("real", core, parent)

	def set(self, sr_ap_map_data_real: float, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, resourceSetNull=repcap.ResourceSetNull.Default, resourceNull=repcap.ResourceNull.Default, accessPointNull=repcap.AccessPointNull.Default, rowNull=repcap.RowNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:UL:BWP<BWP(DIR0)>:SRS:RS:SET<GR0>:RES<USER0>:APMap:AP<AP(S2US0)>:ROW<APR(S3US0)>:REAL \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.uplink.bwp.srs.rs.set.res.apMap.ap.row.real.set(sr_ap_map_data_real = 1.0, userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, resourceSetNull = repcap.ResourceSetNull.Default, resourceNull = repcap.ResourceNull.Default, accessPointNull = repcap.AccessPointNull.Default, rowNull = repcap.RowNull.Default) \n
		Define the mapping of the antenna ports to the physical antennas. \n
			:param sr_ap_map_data_real: float The REAL (magnitude) and IMAGinary (phase) values are interdependent. Their value ranges change depending on each other and so that the resulting complex value is as follows: |REAL+j*IMAGinary| <= 1 Otherwise, the values are normalized to magnitude = 1. Range: -1 to 1
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param resourceSetNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param resourceNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param accessPointNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Ap')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
		"""
		param = Conversions.decimal_value_to_str(sr_ap_map_data_real)
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		resourceSetNull_cmd_val = self._cmd_group.get_repcap_cmd_value(resourceSetNull, repcap.ResourceSetNull)
		resourceNull_cmd_val = self._cmd_group.get_repcap_cmd_value(resourceNull, repcap.ResourceNull)
		accessPointNull_cmd_val = self._cmd_group.get_repcap_cmd_value(accessPointNull, repcap.AccessPointNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:UL:BWP{bwPartNull_cmd_val}:SRS:RS:SET{resourceSetNull_cmd_val}:RES{resourceNull_cmd_val}:APMap:AP{accessPointNull_cmd_val}:ROW{rowNull_cmd_val}:REAL {param}')

	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, resourceSetNull=repcap.ResourceSetNull.Default, resourceNull=repcap.ResourceNull.Default, accessPointNull=repcap.AccessPointNull.Default, rowNull=repcap.RowNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<US(CH0)>:CELL<CC(ST0)>:UL:BWP<BWP(DIR0)>:SRS:RS:SET<GR0>:RES<USER0>:APMap:AP<AP(S2US0)>:ROW<APR(S3US0)>:REAL \n
		Snippet: value: float = driver.source.bb.nr5G.ubwp.user.cell.uplink.bwp.srs.rs.set.res.apMap.ap.row.real.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, resourceSetNull = repcap.ResourceSetNull.Default, resourceNull = repcap.ResourceNull.Default, accessPointNull = repcap.AccessPointNull.Default, rowNull = repcap.RowNull.Default) \n
		Define the mapping of the antenna ports to the physical antennas. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param resourceSetNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Set')
			:param resourceNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:param accessPointNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Ap')
			:param rowNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Row')
			:return: sr_ap_map_data_real: float The REAL (magnitude) and IMAGinary (phase) values are interdependent. Their value ranges change depending on each other and so that the resulting complex value is as follows: |REAL+j*IMAGinary| <= 1 Otherwise, the values are normalized to magnitude = 1. Range: -1 to 1"""
		userNull_cmd_val = self._cmd_group.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		resourceSetNull_cmd_val = self._cmd_group.get_repcap_cmd_value(resourceSetNull, repcap.ResourceSetNull)
		resourceNull_cmd_val = self._cmd_group.get_repcap_cmd_value(resourceNull, repcap.ResourceNull)
		accessPointNull_cmd_val = self._cmd_group.get_repcap_cmd_value(accessPointNull, repcap.AccessPointNull)
		rowNull_cmd_val = self._cmd_group.get_repcap_cmd_value(rowNull, repcap.RowNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:UL:BWP{bwPartNull_cmd_val}:SRS:RS:SET{resourceSetNull_cmd_val}:RES{resourceNull_cmd_val}:APMap:AP{accessPointNull_cmd_val}:ROW{rowNull_cmd_val}:REAL?')
		return Conversions.str_to_float(response)
