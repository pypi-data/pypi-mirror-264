from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConfigCls:
	"""Config commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("config", core, parent)

	def set(self, fe_type_unused: List[str], ip_or_pcname: str, dev_id: str, symb_name: str) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:CONNection:CONFig \n
		Snippet: driver.source.efrontend.connection.config.set(fe_type_unused = ['abc1', 'abc2', 'abc3'], ip_or_pcname = 'abc', dev_id = 'abc', symb_name = 'abc') \n
		No command help available \n
			:param fe_type_unused: No help available
			:param ip_or_pcname: No help available
			:param dev_id: No help available
			:param symb_name: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle.as_open_list('fe_type_unused', fe_type_unused, DataType.StringList, None), ArgSingle('ip_or_pcname', ip_or_pcname, DataType.String), ArgSingle('dev_id', dev_id, DataType.String), ArgSingle('symb_name', symb_name, DataType.String))
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:CONNection:CONFig {param}'.rstrip())
