from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CustomerCls:
	"""Customer commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("customer", core, parent)

	def get_mapping(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:HDR:CUSTomer:MAPping \n
		Snippet: value: bool = driver.source.bb.btooth.hdr.customer.get_mapping() \n
		No command help available \n
			:return: custom_mapp: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:HDR:CUSTomer:MAPping?')
		return Conversions.str_to_bool(response)

	def set_mapping(self, custom_mapp: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:HDR:CUSTomer:MAPping \n
		Snippet: driver.source.bb.btooth.hdr.customer.set_mapping(custom_mapp = False) \n
		No command help available \n
			:param custom_mapp: No help available
		"""
		param = Conversions.bool_to_str(custom_mapp)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:HDR:CUSTomer:MAPping {param}')
