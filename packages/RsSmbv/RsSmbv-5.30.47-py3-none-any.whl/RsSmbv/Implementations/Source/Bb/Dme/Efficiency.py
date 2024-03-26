from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EfficiencyCls:
	"""Efficiency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("efficiency", core, parent)

	# noinspection PyTypeChecker
	def get_replies(self) -> enums.AvionicDmeReplCount:
		"""SCPI: [SOURce<HW>]:[BB]:DME:EFFiciency:REPLies \n
		Snippet: value: enums.AvionicDmeReplCount = driver.source.bb.dme.efficiency.get_replies() \n
		Sets the number of reply pulses. Use this number to specify absolute values of false or correct pulses during reply
		efficiency measurements. \n
			:return: no_of_replies: 10| 50| 100 10, 50 or 100 reply pulses
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:EFFiciency:REPLies?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmeReplCount)

	def set_replies(self, no_of_replies: enums.AvionicDmeReplCount) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:EFFiciency:REPLies \n
		Snippet: driver.source.bb.dme.efficiency.set_replies(no_of_replies = enums.AvionicDmeReplCount._10) \n
		Sets the number of reply pulses. Use this number to specify absolute values of false or correct pulses during reply
		efficiency measurements. \n
			:param no_of_replies: 10| 50| 100 10, 50 or 100 reply pulses
		"""
		param = Conversions.enum_scalar_to_str(no_of_replies, enums.AvionicDmeReplCount)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:EFFiciency:REPLies {param}')

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:[BB]:DME:EFFiciency \n
		Snippet: value: int = driver.source.bb.dme.efficiency.get_value() \n
		Sets the relation between reply pulse pairs and received trigger signals, e.g. with a set efficiency of 50% only every
		second trigger event leads to the generation of a reply pulse pair. \n
			:return: efficiency: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:EFFiciency?')
		return Conversions.str_to_int(response)

	def set_value(self, efficiency: int) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:EFFiciency \n
		Snippet: driver.source.bb.dme.efficiency.set_value(efficiency = 1) \n
		Sets the relation between reply pulse pairs and received trigger signals, e.g. with a set efficiency of 50% only every
		second trigger event leads to the generation of a reply pulse pair. \n
			:param efficiency: integer Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(efficiency)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:EFFiciency {param}')
