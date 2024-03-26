from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyncCls:
	"""Sync commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sync", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:PULM:OUTPut:SYNC:[STATe] \n
		Snippet: value: bool = driver.source.pulm.output.sync.get_state() \n
		Routes the pulse modulation signal to the [Signal Valid] connector. \n
			:return: sync: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:OUTPut:SYNC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, sync: bool) -> None:
		"""SCPI: [SOURce<HW>]:PULM:OUTPut:SYNC:[STATe] \n
		Snippet: driver.source.pulm.output.sync.set_state(sync = False) \n
		Routes the pulse modulation signal to the [Signal Valid] connector. \n
			:param sync: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(sync)
		self._core.io.write(f'SOURce<HwInstance>:PULM:OUTPut:SYNC:STATe {param}')
