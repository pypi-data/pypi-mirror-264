from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:VOR:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.vor.setting.get_catalog() \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.ils/*.vor/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: avionic_vor_cat_names: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:VOR:SETTing:DELete \n
		Snippet: driver.source.bb.vor.setting.delete(filename = 'abc') \n
		Deletes the selected file from the default or the specified directory. Deleted are files with extension *.ils/*.vor/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:VOR:SETTing:LOAD \n
		Snippet: driver.source.bb.vor.setting.load(filename = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.ils/*.vor/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:VOR:SETTing:STORe \n
		Snippet: driver.source.bb.vor.setting.set_store(filename = 'abc') \n
		Saves the current settings into the selected file; the file extension (*.ils/*.vor/*.dme) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:SETTing:STORe {param}')
