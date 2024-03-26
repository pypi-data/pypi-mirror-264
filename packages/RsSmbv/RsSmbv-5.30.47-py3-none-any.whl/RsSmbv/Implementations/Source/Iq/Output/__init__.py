from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 90 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	@property
	def analog(self):
		"""analog commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_analog'):
			from .Analog import AnalogCls
			self._analog = AnalogCls(self._core, self._cmd_group)
		return self._analog

	@property
	def digital(self):
		"""digital commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import DigitalCls
			self._digital = DigitalCls(self._core, self._cmd_group)
		return self._digital

	def get_level(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:LEVel \n
		Snippet: value: float = driver.source.iq.output.get_level() \n
		Sets the off-load voltage Vp of the analog I/Q signal output. The value range is adjusted so that the maximum overall
		output voltage does not exceed 4V, see 'Maximum overall output voltage'. Also, the value range depends on the installed
		options, see the data sheet. \n
			:return: level: float Range: depends on options to 4, Unit: V
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:LEVel \n
		Snippet: driver.source.iq.output.set_level(level = 1.0) \n
		Sets the off-load voltage Vp of the analog I/Q signal output. The value range is adjusted so that the maximum overall
		output voltage does not exceed 4V, see 'Maximum overall output voltage'. Also, the value range depends on the installed
		options, see the data sheet. \n
			:param level: float Range: depends on options to 4, Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:LEVel {param}')

	def clone(self) -> 'OutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
