from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	def set(self, power: float, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:RF:POWer \n
		Snippet: driver.sconfiguration.external.hsDigital.rf.power.set(power = 1.0, index = repcap.Index.Default) \n
		In uncoupled mode, sets the RF level of the external instrument. \n
			:param power: float Range: -130 to 20
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
		"""
		param = Conversions.decimal_value_to_str(power)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:RF:POWer {param}')

	def get(self, index=repcap.Index.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:RF:POWer \n
		Snippet: value: float = driver.sconfiguration.external.hsDigital.rf.power.get(index = repcap.Index.Default) \n
		In uncoupled mode, sets the RF level of the external instrument. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
			:return: power: float Range: -130 to 20"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:RF:POWer?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'PowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
