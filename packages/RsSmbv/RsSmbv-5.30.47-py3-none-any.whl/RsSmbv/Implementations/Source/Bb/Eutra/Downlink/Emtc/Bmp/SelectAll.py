from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectAllCls:
	"""SelectAll commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("selectAll", core, parent)

	def set(self, selectAllNull=repcap.SelectAllNull.Nr0) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:SELectlall<ST0> \n
		Snippet: driver.source.bb.eutra.downlink.emtc.bmp.selectAll.set(selectAllNull = repcap.SelectAllNull.Nr0) \n
		Sets all SFs as valid or invalid. \n
			:param selectAllNull: optional repeated capability selector. Default value: Nr0
		"""
		selectAllNull_cmd_val = self._cmd_group.get_repcap_cmd_value(selectAllNull, repcap.SelectAllNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:SELectlall{selectAllNull_cmd_val}')

	def set_with_opc(self, selectAllNull=repcap.SelectAllNull.Nr0, opc_timeout_ms: int = -1) -> None:
		selectAllNull_cmd_val = self._cmd_group.get_repcap_cmd_value(selectAllNull, repcap.SelectAllNull)
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:SELectlall<ST0> \n
		Snippet: driver.source.bb.eutra.downlink.emtc.bmp.selectAll.set_with_opc(selectAllNull = repcap.SelectAllNull.Nr0) \n
		Sets all SFs as valid or invalid. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param selectAllNull: optional repeated capability selector. Default value: Nr0
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:SELectlall{selectAllNull_cmd_val}', opc_timeout_ms)
