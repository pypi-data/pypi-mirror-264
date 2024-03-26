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
		"""SCPI: [SOURce<HW>]:BB:GBAS:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.gbas.setting.get_catalog() \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.gbas.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:return: catalog: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:SETTing:DELete \n
		Snippet: driver.source.bb.gbas.setting.delete(filename = 'abc') \n
		Deletes the selected file from the default or the specified directory. Deleted are files with extension *.gbas. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:SETTing:LOAD \n
		Snippet: driver.source.bb.gbas.setting.load(filename = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.gbas. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:SETTing:STORe \n
		Snippet: driver.source.bb.gbas.setting.set_store(filename = 'abc') \n
		Saves the current settings into the selected file; the file extension (*.gbas) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:SETTing:STORe {param}')
