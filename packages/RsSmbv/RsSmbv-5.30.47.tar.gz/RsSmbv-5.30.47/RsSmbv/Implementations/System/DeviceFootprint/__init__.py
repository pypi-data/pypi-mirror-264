from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeviceFootprintCls:
	"""DeviceFootprint commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("deviceFootprint", core, parent)

	@property
	def history(self):
		"""history commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_history'):
			from .History import HistoryCls
			self._history = HistoryCls(self._core, self._cmd_group)
		return self._history

	def set(self, directory: str) -> None:
		"""SCPI: SYSTem:DFPRint \n
		Snippet: driver.system.deviceFootprint.set(directory = 'abc') \n
		Queries the device footprint of the instrument. The retrieved information is in machine-readable form suitable for
		automatic further processing. \n
			:param directory: No help available
		"""
		param = Conversions.value_to_quoted_str(directory)
		self._core.io.write(f'SYSTem:DFPRint {param}')

	def get(self) -> str:
		"""SCPI: SYSTem:DFPRint \n
		Snippet: value: str = driver.system.deviceFootprint.get() \n
		Queries the device footprint of the instrument. The retrieved information is in machine-readable form suitable for
		automatic further processing. \n
			:return: device_footprint: string Information on the instrument type, device identification and details on the installed FW version, hardware and software options."""
		response = self._core.io.query_str(f'SYSTem:DFPRint?')
		return trim_str_response(response)

	def clone(self) -> 'DeviceFootprintCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DeviceFootprintCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
