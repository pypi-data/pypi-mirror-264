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

	def set(self, frequency: float, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:RF:FREQuency \n
		Snippet: driver.sconfiguration.external.hsDigital.rf.frequency.set(frequency = 1.0, index = repcap.Index.Default) \n
		In uncoupled mode, sets the RF frequency of the external instrument. \n
			:param frequency: float Range: 100E3 to 3E9
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
		"""
		param = Conversions.decimal_value_to_str(frequency)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:RF:FREQuency {param}')

	def get(self, index=repcap.Index.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:RF:FREQuency \n
		Snippet: value: float = driver.sconfiguration.external.hsDigital.rf.frequency.get(index = repcap.Index.Default) \n
		In uncoupled mode, sets the RF frequency of the external instrument. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
			:return: frequency: float Range: 100E3 to 3E9"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:RF:FREQuency?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'FrequencyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrequencyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
