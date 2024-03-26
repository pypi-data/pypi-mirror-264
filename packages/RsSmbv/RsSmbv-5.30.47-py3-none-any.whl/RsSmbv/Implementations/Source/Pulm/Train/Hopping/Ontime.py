from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OntimeCls:
	"""Ontime commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ontime", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:ONTime:POINts \n
		Snippet: value: int = driver.source.pulm.train.hopping.ontime.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:ONTime:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:ONTime \n
		Snippet: value: str = driver.source.pulm.train.hopping.ontime.get_value() \n
		No command help available \n
			:return: ontime: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TRAin:HOPPing:ONTime?')
		return trim_str_response(response)

	def set_value(self, ontime: str) -> None:
		"""SCPI: [SOURce<HW>]:PULM:TRAin:HOPPing:ONTime \n
		Snippet: driver.source.pulm.train.hopping.ontime.set_value(ontime = 'abc') \n
		No command help available \n
			:param ontime: No help available
		"""
		param = Conversions.value_to_quoted_str(ontime)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TRAin:HOPPing:ONTime {param}')
