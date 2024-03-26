from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfOffsetCls:
	"""SfOffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sfOffset", core, parent)

	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:MIB:SFOFfset \n
		Snippet: value: int = driver.source.bb.nr5G.node.cell.sspbch.mib.sfOffset.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		By default, the counting of the SFN (system frame number) starts with 0. Use this parameter to set a different start SFN
		value. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: ssp_bch_sf_start_of: integer Range: 0 to 1023"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:MIB:SFOFfset?')
		return Conversions.str_to_int(response)
