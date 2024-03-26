from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsCls:
	"""Cs commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cs", core, parent)

	# noinspection PyTypeChecker
	def get_dip(self) -> enums.TcwDip:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:CS:DIP \n
		Snippet: value: enums.TcwDip = driver.source.bb.eutra.tcw.cs.get_dip() \n
		No command help available \n
			:return: dip_set: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:CS:DIP?')
		return Conversions.str_to_scalar_enum(response, enums.TcwDip)

	def set_dip(self, dip_set: enums.TcwDip) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:CS:DIP \n
		Snippet: driver.source.bb.eutra.tcw.cs.set_dip(dip_set = enums.TcwDip.SET1) \n
		No command help available \n
			:param dip_set: No help available
		"""
		param = Conversions.enum_scalar_to_str(dip_set, enums.TcwDip)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:CS:DIP {param}')

	# noinspection PyTypeChecker
	def get_rpow(self) -> enums.TcwDip:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:CS:RPOW \n
		Snippet: value: enums.TcwDip = driver.source.bb.eutra.tcw.cs.get_rpow() \n
		No command help available \n
			:return: relative_power: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:CS:RPOW?')
		return Conversions.str_to_scalar_enum(response, enums.TcwDip)
