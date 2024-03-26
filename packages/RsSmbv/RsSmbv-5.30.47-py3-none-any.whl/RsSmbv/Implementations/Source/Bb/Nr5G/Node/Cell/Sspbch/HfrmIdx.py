from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HfrmIdxCls:
	"""HfrmIdx commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hfrmIdx", core, parent)

	def set(self, half_frame_idx: int, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:HFRMidx \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.hfrmIdx.set(half_frame_idx = 1, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines in which half-frame of the time plan the first SS/PBCH burst occasion is located. The 'Half Frame Index' value
		depends on the configured 'Burst Set Periodicity'. The default value is 0, it locates the first SS/PBCH occasion in the
		first half-frame. If you set the value to 1, the first SS/PBCH occasion is in the second half-frame and so forth. \n
			:param half_frame_idx: integer Range: 0 to 31
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.decimal_value_to_str(half_frame_idx)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:HFRMidx {param}')

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:HFRMidx \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.sspbch.hfrmIdx.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Defines in which half-frame of the time plan the first SS/PBCH burst occasion is located. The 'Half Frame Index' value
		depends on the configured 'Burst Set Periodicity'. The default value is 0, it locates the first SS/PBCH occasion in the
		first half-frame. If you set the value to 1, the first SS/PBCH occasion is in the second half-frame and so forth. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: half_frame_idx: integer Range: 0 to 31"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:HFRMidx?')
		return Conversions.str_to_int(response)
