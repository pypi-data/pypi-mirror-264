from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SffmCls:
	"""Sffm commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sffm", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:SFFM:STATe \n
		Snippet: value: bool = driver.source.bb.nr5G.qckset.general.sffm.get_state() \n
		Turns synchronization to the marker on and off. \n
			:return: sync_to_marker: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:SFFM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, sync_to_marker: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:GENeral:SFFM:STATe \n
		Snippet: driver.source.bb.nr5G.qckset.general.sffm.set_state(sync_to_marker = False) \n
		Turns synchronization to the marker on and off. \n
			:param sync_to_marker: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(sync_to_marker)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:SFFM:STATe {param}')
