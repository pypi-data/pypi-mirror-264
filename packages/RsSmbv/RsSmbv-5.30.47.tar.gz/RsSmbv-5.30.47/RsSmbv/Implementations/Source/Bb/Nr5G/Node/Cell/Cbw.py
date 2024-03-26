from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CbwCls:
	"""Cbw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cbw", core, parent)

	def set(self, chan_bandwidth: enums.Nr5Gcbw, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:CBW \n
		Snippet: driver.source.bb.nr5G.node.cell.cbw.set(chan_bandwidth = enums.Nr5Gcbw.BW10, cellNull = repcap.CellNull.Default) \n
		Selects the bandwidth of the node carrier. Some bandwidths are available with R&S SMBVB-K171. \n
			:param chan_bandwidth: BW5 | BW10 | BW15 | BW20 | BW25 | BW30 | BW35 | BW40 | BW45 | BW50 | BW60 | BW70 | BW80 | BW90 | BW100 | BW200 | BW400 | BW800 | BW1600 | BW2000
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.enum_scalar_to_str(chan_bandwidth, enums.Nr5Gcbw)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:CBW {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.Nr5Gcbw:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:CBW \n
		Snippet: value: enums.Nr5Gcbw = driver.source.bb.nr5G.node.cell.cbw.get(cellNull = repcap.CellNull.Default) \n
		Selects the bandwidth of the node carrier. Some bandwidths are available with R&S SMBVB-K171. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: chan_bandwidth: BW5 | BW10 | BW15 | BW20 | BW25 | BW30 | BW35 | BW40 | BW45 | BW50 | BW60 | BW70 | BW80 | BW90 | BW100 | BW200 | BW400 | BW800 | BW1600 | BW2000"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:CBW?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5Gcbw)
