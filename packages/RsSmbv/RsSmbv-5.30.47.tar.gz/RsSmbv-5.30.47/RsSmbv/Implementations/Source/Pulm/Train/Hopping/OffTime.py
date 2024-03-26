from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffTimeCls:
	"""OffTime commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offTime", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:OFFTime:POINts \n
		Snippet: value: int = driver.source.pulm.train.hopping.offTime.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:OFFTime:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:OFFTime \n
		Snippet: value: str = driver.source.pulm.train.hopping.offTime.get_value() \n
		No command help available \n
			:return: off_time: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:OFFTime?')
		return trim_str_response(response)

	def set_value(self, off_time: str) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:OFFTime \n
		Snippet: driver.source.pulm.train.hopping.offTime.set_value(off_time = 'abc') \n
		No command help available \n
			:param off_time: No help available
		"""
		param = Conversions.value_to_quoted_str(off_time)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:HOPPing:OFFTime {param}')
