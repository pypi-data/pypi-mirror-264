from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def get_ok(self) -> bool:
		"""SCPI: [SOURce<HW>]:[BB]:DME:PINPut:TRIGger:LEVel:OK \n
		Snippet: value: bool = driver.source.bb.dme.pinput.trigger.level.get_ok() \n
		Queries, if the search trigger level procedure determines a valid trigger level or not. Use this query for quick check,
		if there is a valid trigger level without running the search trigger level procedure via the following command: \n
			:return: is_trig_lev_ok: 1| ON| 0| OFF 1|ON Valid trigger level 0|OFF Invalid trigger level
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PINPut:TRIGger:LEVel:OK?')
		return Conversions.str_to_bool(response)

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:PINPut:TRIGger:LEVel \n
		Snippet: value: float = driver.source.bb.dme.pinput.trigger.level.get_value() \n
		Queries the last measured value of the trigger power level. This level is the 50% voltage point of the first pulse of the
		external DME interrogation signal. \n
			:return: trigger_level: float Range: -200 to 200
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PINPut:TRIGger:LEVel?')
		return Conversions.str_to_float(response)
