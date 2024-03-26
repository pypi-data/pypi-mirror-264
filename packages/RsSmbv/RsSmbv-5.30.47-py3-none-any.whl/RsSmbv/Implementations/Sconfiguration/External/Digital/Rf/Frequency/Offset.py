from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, freq_offset: float, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:RF:FREQuency:OFFSet \n
		Snippet: driver.sconfiguration.external.digital.rf.frequency.offset.set(freq_offset = 1.0, index = repcap.Index.Default) \n
		In coupled mode, offsets the RF frequency of the external instrument with the selected delta value. \n
			:param freq_offset: float Range: -3E9 to 3E9
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
		"""
		param = Conversions.decimal_value_to_str(freq_offset)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:RF:FREQuency:OFFSet {param}')

	def get(self, index=repcap.Index.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:RF:FREQuency:OFFSet \n
		Snippet: value: float = driver.sconfiguration.external.digital.rf.frequency.offset.get(index = repcap.Index.Default) \n
		In coupled mode, offsets the RF frequency of the external instrument with the selected delta value. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:return: freq_offset: float Range: -3E9 to 3E9"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:RF:FREQuency:OFFSet?')
		return Conversions.str_to_float(response)
