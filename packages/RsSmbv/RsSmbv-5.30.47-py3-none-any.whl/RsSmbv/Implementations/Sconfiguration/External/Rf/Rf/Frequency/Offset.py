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

	def set(self, freq_offset: float, path=repcap.Path.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:FREQuency:OFFSet \n
		Snippet: driver.sconfiguration.external.rf.rf.frequency.offset.set(freq_offset = 1.0, path = repcap.Path.Default) \n
		No command help available \n
			:param freq_offset: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = Conversions.decimal_value_to_str(freq_offset)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:FREQuency:OFFSet {param}')

	def get(self, path=repcap.Path.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:FREQuency:OFFSet \n
		Snippet: value: float = driver.sconfiguration.external.rf.rf.frequency.offset.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: freq_offset: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:FREQuency:OFFSet?')
		return Conversions.str_to_float(response)
