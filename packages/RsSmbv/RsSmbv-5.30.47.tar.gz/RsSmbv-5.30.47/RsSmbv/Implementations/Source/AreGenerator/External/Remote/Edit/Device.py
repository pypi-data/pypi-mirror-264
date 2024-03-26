from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeviceCls:
	"""Device commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("device", core, parent)

	def get_id(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:DEVice:[ID] \n
		Snippet: value: str = driver.source.areGenerator.external.remote.edit.device.get_id() \n
		No command help available \n
			:return: device_id: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:DEVice:ID?')
		return trim_str_response(response)

	def set_id(self, device_id: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:DEVice:[ID] \n
		Snippet: driver.source.areGenerator.external.remote.edit.device.set_id(device_id = 'abc') \n
		No command help available \n
			:param device_id: No help available
		"""
		param = Conversions.value_to_quoted_str(device_id)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:DEVice:ID {param}')
