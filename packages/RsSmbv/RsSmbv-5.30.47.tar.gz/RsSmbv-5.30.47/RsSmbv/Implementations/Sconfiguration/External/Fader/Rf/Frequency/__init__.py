from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	def set(self, frequency: float, digitalIq=repcap.DigitalIq.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:RF:FREQuency \n
		Snippet: driver.sconfiguration.external.fader.rf.frequency.set(frequency = 1.0, digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param frequency: No help available
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
		"""
		param = Conversions.decimal_value_to_str(frequency)
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		self._core.io.write(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:RF:FREQuency {param}')

	def get(self, digitalIq=repcap.DigitalIq.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:RF:FREQuency \n
		Snippet: value: float = driver.sconfiguration.external.fader.rf.frequency.get(digitalIq = repcap.DigitalIq.Default) \n
		No command help available \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: frequency: No help available"""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:RF:FREQuency?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'FrequencyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrequencyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
