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

	def set(self, freq_offset: float, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:RF:FREQuency:OFFSet \n
		Snippet: driver.sconfiguration.external.bbmm.rf.frequency.offset.set(freq_offset = 1.0, iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param freq_offset: No help available
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = Conversions.decimal_value_to_str(freq_offset)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:RF:FREQuency:OFFSet {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:RF:FREQuency:OFFSet \n
		Snippet: value: float = driver.sconfiguration.external.bbmm.rf.frequency.offset.get(iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
			:return: freq_offset: No help available"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:RF:FREQuency:OFFSet?')
		return Conversions.str_to_float(response)
