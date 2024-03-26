from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcCls:
	"""Cc commands group definition. 7 total commands, 1 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cc", core, parent)

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .Add import AddCls
			self._add = AddCls(self._core, self._cmd_group)
		return self._add

	def get_cinfo(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:CINFo \n
		Snippet: value: str = driver.source.bb.nr5G.node.cc.get_cinfo() \n
		Queries basic information about the carrier you want to duplicate.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a file as the source of the new carrier ([:SOURce<hw>]:BB:NR5G:NODE:CC:CPYSel) . \n
			:return: sel_carrier_info: string String containing the information about the carrier.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:CC:CINFo?')
		return trim_str_response(response)

	def get_cpy_from(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:CPYFrom \n
		Snippet: value: int = driver.source.bb.nr5G.node.cc.get_cpy_from() \n
		Selects the carrier you want to duplicate.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Selecting a carrier is only possible if there are more than one carrier in the table or in the configuration file. \n
			:return: copy_from: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:CC:CPYFrom?')
		return Conversions.str_to_int(response)

	def set_cpy_from(self, copy_from: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:CPYFrom \n
		Snippet: driver.source.bb.nr5G.node.cc.set_cpy_from(copy_from = 1) \n
		Selects the carrier you want to duplicate.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Selecting a carrier is only possible if there are more than one carrier in the table or in the configuration file. \n
			:param copy_from: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(copy_from)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CC:CPYFrom {param}')

	# noinspection PyTypeChecker
	def get_cpy_sel(self) -> enums.CopySelection:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:CPYSel \n
		Snippet: value: enums.CopySelection = driver.source.bb.nr5G.node.cc.get_cpy_sel() \n
		Selects the source of a carrier that you want to create based on an existing carrier. \n
			:return: copy_selection: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:CC:CPYSel?')
		return Conversions.str_to_scalar_enum(response, enums.CopySelection)

	def set_cpy_sel(self, copy_selection: enums.CopySelection) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:CPYSel \n
		Snippet: driver.source.bb.nr5G.node.cc.set_cpy_sel(copy_selection = enums.CopySelection.CARRier) \n
		Selects the source of a carrier that you want to create based on an existing carrier. \n
			:param copy_selection: CARRier Carrier from the current carrier table. LOADfile Carrier from a previously saved signal configuration (.nr5g file) .
		"""
		param = Conversions.enum_scalar_to_str(copy_selection, enums.CopySelection)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CC:CPYSel {param}')

	def get_cpy_to(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:CPYTo \n
		Snippet: value: str = driver.source.bb.nr5G.node.cc.get_cpy_to() \n
		Queries the index number the new carriers are created with. \n
			:return: copy_from: string String containing the number of the new carriers.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:CC:CPYTo?')
		return trim_str_response(response)

	def get_load(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:LOAD \n
		Snippet: value: str = driver.source.bb.nr5G.node.cc.get_load() \n
		Selects a file containing an existing carrier you want to duplicate.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a file as the source of the new carrier ([:SOURce<hw>]:BB:NR5G:NODE:CC:CPYSel) . \n
			:return: filename: string String containing the file name.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:CC:LOAD?')
		return trim_str_response(response)

	def set_load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:LOAD \n
		Snippet: driver.source.bb.nr5G.node.cc.set_load(filename = 'abc') \n
		Selects a file containing an existing carrier you want to duplicate.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select a file as the source of the new carrier ([:SOURce<hw>]:BB:NR5G:NODE:CC:CPYSel) . \n
			:param filename: string String containing the file name.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CC:LOAD {param}')

	def get_new_carriers(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:NEWCarriers \n
		Snippet: value: int = driver.source.bb.nr5G.node.cc.get_new_carriers() \n
		Defines the number of carriers you want to create based on an existing carrier. \n
			:return: num_of_new: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:CC:NEWCarriers?')
		return Conversions.str_to_int(response)

	def set_new_carriers(self, num_of_new: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CC:NEWCarriers \n
		Snippet: driver.source.bb.nr5G.node.cc.set_new_carriers(num_of_new = 1) \n
		Defines the number of carriers you want to create based on an existing carrier. \n
			:param num_of_new: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(num_of_new)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CC:NEWCarriers {param}')

	def clone(self) -> 'CcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
