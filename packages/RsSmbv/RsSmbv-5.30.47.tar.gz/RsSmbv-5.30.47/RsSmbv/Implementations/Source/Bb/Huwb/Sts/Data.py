from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	def get_dselection(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:DATA:DSELection \n
		Snippet: value: str = driver.source.bb.huwb.sts.data.get_dselection() \n
		Selects an existing data list file from the default directory or from a specific directory. The data list is only used,
		if DLS is activated. \n
			:return: sts_dlist: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STS:DATA:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, sts_dlist: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:STS:DATA:DSELection \n
		Snippet: driver.source.bb.huwb.sts.data.set_dselection(sts_dlist = 'abc') \n
		Selects an existing data list file from the default directory or from a specific directory. The data list is only used,
		if DLS is activated. \n
			:param sts_dlist: string
		"""
		param = Conversions.value_to_quoted_str(sts_dlist)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STS:DATA:DSELection {param}')
