from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PkeyCls:
	"""Pkey commands group definition. 4 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pkey", core, parent)

	@property
	def tduration(self):
		"""tduration commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tduration'):
			from .Tduration import TdurationCls
			self._tduration = TdurationCls(self._core, self._cmd_group)
		return self._tduration

	def get_nt_day(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:NTDay \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.pkey.get_nt_day() \n
		No command help available \n
			:return: trans_per_day: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:NTDay?')
		return Conversions.str_to_int(response)

	def set_nt_day(self, trans_per_day: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:NTDay \n
		Snippet: driver.source.bb.gnss.galileo.osnma.pkey.set_nt_day(trans_per_day = 1) \n
		No command help available \n
			:param trans_per_day: No help available
		"""
		param = Conversions.decimal_value_to_str(trans_per_day)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:NTDay {param}')

	def get_to_midnight(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:TOMidnight \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.pkey.get_to_midnight() \n
		No command help available \n
			:return: time_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:TOMidnight?')
		return Conversions.str_to_int(response)

	def set_to_midnight(self, time_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PKEY:TOMidnight \n
		Snippet: driver.source.bb.gnss.galileo.osnma.pkey.set_to_midnight(time_offset = 1) \n
		No command help available \n
			:param time_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(time_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PKEY:TOMidnight {param}')

	def clone(self) -> 'PkeyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PkeyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
