from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MhdtCls:
	"""Mhdt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mhdt", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:MHDT:STATe \n
		Snippet: value: bool = driver.source.bb.btooth.mhdt.get_state() \n
		No command help available \n
			:return: mhdt_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:MHDT:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, mhdt_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:MHDT:STATe \n
		Snippet: driver.source.bb.btooth.mhdt.set_state(mhdt_state = False) \n
		No command help available \n
			:param mhdt_state: No help available
		"""
		param = Conversions.bool_to_str(mhdt_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:MHDT:STATe {param}')
