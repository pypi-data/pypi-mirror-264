from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ResolveCls:
	"""Resolve commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("resolve", core, parent)

	def set(self, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TXBW:RESolve \n
		Snippet: driver.source.bb.nr5G.node.cell.txbw.resolve.set(cellNull = repcap.CellNull.Default) \n
		Recalculates the frequency-dependent settings and thus redefines the frequency position of the TxBW. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TXBW:RESolve')

	def set_with_opc(self, cellNull=repcap.CellNull.Default, opc_timeout_ms: int = -1) -> None:
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:TXBW:RESolve \n
		Snippet: driver.source.bb.nr5G.node.cell.txbw.resolve.set_with_opc(cellNull = repcap.CellNull.Default) \n
		Recalculates the frequency-dependent settings and thus redefines the frequency position of the TxBW. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:TXBW:RESolve', opc_timeout_ms)
