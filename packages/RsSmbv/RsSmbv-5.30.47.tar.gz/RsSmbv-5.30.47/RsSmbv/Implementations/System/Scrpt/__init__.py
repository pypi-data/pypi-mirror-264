from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScrptCls:
	"""Scrpt commands group definition. 5 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scrpt", core, parent)

	@property
	def discard(self):
		"""discard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_discard'):
			from .Discard import DiscardCls
			self._discard = DiscardCls(self._core, self._cmd_group)
		return self._discard

	def get_arg(self) -> str:
		"""SCPI: SYSTem:SCRPt:ARG \n
		Snippet: value: str = driver.system.scrpt.get_arg() \n
		No command help available \n
			:return: arguments: No help available
		"""
		response = self._core.io.query_str('SYSTem:SCRPt:ARG?')
		return trim_str_response(response)

	def set_arg(self, arguments: str) -> None:
		"""SCPI: SYSTem:SCRPt:ARG \n
		Snippet: driver.system.scrpt.set_arg(arguments = 'abc') \n
		No command help available \n
			:param arguments: No help available
		"""
		param = Conversions.value_to_quoted_str(arguments)
		self._core.io.write(f'SYSTem:SCRPt:ARG {param}')

	def get_cmd(self) -> str:
		"""SCPI: SYSTem:SCRPt:CMD \n
		Snippet: value: str = driver.system.scrpt.get_cmd() \n
		No command help available \n
			:return: cmd_file: No help available
		"""
		response = self._core.io.query_str('SYSTem:SCRPt:CMD?')
		return trim_str_response(response)

	def set_cmd(self, cmd_file: str) -> None:
		"""SCPI: SYSTem:SCRPt:CMD \n
		Snippet: driver.system.scrpt.set_cmd(cmd_file = 'abc') \n
		No command help available \n
			:param cmd_file: No help available
		"""
		param = Conversions.value_to_quoted_str(cmd_file)
		self._core.io.write(f'SYSTem:SCRPt:CMD {param}')

	def get_data(self) -> str:
		"""SCPI: SYSTem:SCRPt:DATA \n
		Snippet: value: str = driver.system.scrpt.get_data() \n
		No command help available \n
			:return: data_file: No help available
		"""
		response = self._core.io.query_str('SYSTem:SCRPt:DATA?')
		return trim_str_response(response)

	def set_data(self, data_file: str) -> None:
		"""SCPI: SYSTem:SCRPt:DATA \n
		Snippet: driver.system.scrpt.set_data(data_file = 'abc') \n
		No command help available \n
			:param data_file: No help available
		"""
		param = Conversions.value_to_quoted_str(data_file)
		self._core.io.write(f'SYSTem:SCRPt:DATA {param}')

	def run(self) -> None:
		"""SCPI: SYSTem:SCRPt:RUN \n
		Snippet: driver.system.scrpt.run() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:SCRPt:RUN')

	def run_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:SCRPt:RUN \n
		Snippet: driver.system.scrpt.run_with_opc() \n
		No command help available \n
		Same as run, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:SCRPt:RUN', opc_timeout_ms)

	def clone(self) -> 'ScrptCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScrptCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
