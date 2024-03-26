from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:ADF:SETTing:DELete \n
		Snippet: driver.source.adf.setting.delete(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ADF:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:ADF:SETTing:LOAD \n
		Snippet: driver.source.adf.setting.load(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ADF:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:ADF:SETTing:STORe \n
		Snippet: driver.source.adf.setting.set_store(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ADF:SETTing:STORe {param}')
