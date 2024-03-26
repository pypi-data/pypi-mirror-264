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

	def set(self, power_offset: float, digitalIq=repcap.DigitalIq.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:RF:POWer:OFFSet \n
		Snippet: driver.sconfiguration.external.fader.rf.power.offset.set(power_offset = 1.0, digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param power_offset: No help available
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
		"""
		param = Conversions.decimal_value_to_str(power_offset)
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		self._core.io.write(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:RF:POWer:OFFSet {param}')

	def get(self, digitalIq=repcap.DigitalIq.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:RF:POWer:OFFSet \n
		Snippet: value: float = driver.sconfiguration.external.fader.rf.power.offset.get(digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: power_offset: No help available"""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:RF:POWer:OFFSet?')
		return Conversions.str_to_float(response)
