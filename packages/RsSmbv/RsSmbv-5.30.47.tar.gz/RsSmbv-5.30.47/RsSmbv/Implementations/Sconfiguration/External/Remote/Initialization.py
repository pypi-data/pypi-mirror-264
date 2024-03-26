from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InitializationCls:
	"""Initialization commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("initialization", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: SCONfiguration:EXTernal:REMote:INITialization:CATalog \n
		Snippet: value: List[str] = driver.sconfiguration.external.remote.initialization.get_catalog() \n
		Queries the names of the existing initialization files in the default directory. Per default, the instrument saves
		user-defined files in the /var/user/ directory. Use the command method RsSmbv.MassMemory.currentDirectory to change the
		default directory to the currently used one. Only files with extension *.iec are listed. \n
			:return: rf_rem_ctrl_scpi_init_cat_name_user: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:EXTernal:REMote:INITialization:CATalog?')
		return Conversions.str_to_str_list(response)
