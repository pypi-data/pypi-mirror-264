from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HdrCls:
	"""Hdr commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hdr", core, parent)

	@property
	def customer(self):
		"""customer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_customer'):
			from .Customer import CustomerCls
			self._customer = CustomerCls(self._core, self._cmd_group)
		return self._customer

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:HDR:STATe \n
		Snippet: value: bool = driver.source.bb.btooth.hdr.get_state() \n
		No command help available \n
			:return: hdr_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:HDR:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, hdr_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:HDR:STATe \n
		Snippet: driver.source.bb.btooth.hdr.set_state(hdr_state = False) \n
		No command help available \n
			:param hdr_state: No help available
		"""
		param = Conversions.bool_to_str(hdr_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:HDR:STATe {param}')

	def clone(self) -> 'HdrCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HdrCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
