from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HdrCls:
	"""Hdr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hdr", core, parent)

	def get_variation(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:SRATe:HDR:VARiation \n
		Snippet: value: float = driver.source.bb.btooth.symbolRate.hdr.get_variation() \n
		No command help available \n
			:return: hdr_sym_rate_var: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:SRATe:HDR:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, hdr_sym_rate_var: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:SRATe:HDR:VARiation \n
		Snippet: driver.source.bb.btooth.symbolRate.hdr.set_variation(hdr_sym_rate_var = 1.0) \n
		No command help available \n
			:param hdr_sym_rate_var: No help available
		"""
		param = Conversions.decimal_value_to_str(hdr_sym_rate_var)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:SRATe:HDR:VARiation {param}')
