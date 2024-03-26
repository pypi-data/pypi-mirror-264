from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SfdCls:
	"""Sfd commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sfd", core, parent)

	def get_usr_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:HUWB:SFD:USRState \n
		Snippet: value: bool = driver.source.bb.huwb.sfd.get_usr_state() \n
		Enables using SFD indices SFD_5, SFD_6 and SFD_7. \n
			:return: user_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:SFD:USRState?')
		return Conversions.str_to_bool(response)

	def set_usr_state(self, user_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:SFD:USRState \n
		Snippet: driver.source.bb.huwb.sfd.set_usr_state(user_state = False) \n
		Enables using SFD indices SFD_5, SFD_6 and SFD_7. \n
			:param user_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(user_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:SFD:USRState {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.HrpUwbSfdIndex:
		"""SCPI: [SOURce<HW>]:BB:HUWB:SFD \n
		Snippet: value: enums.HrpUwbSfdIndex = driver.source.bb.huwb.sfd.get_value() \n
		Sets the start-of-frame delimiter (SFD) symbol sequence. The indices represent SFD symbol sequences with SFD lengths as
		listed in Table 'SFD: indices and lengths'. SFD: indices and lengths
			Table Header:  \n
			- Index / SFD_0 / SFD_1 / SFD_2 / SFD_3 / SFD_4 / SFD_5 / SFD_6 / SFD_7 / SFD_8
			- SFD / 0 / 1 / 2 / 3 / 4 / User1 / User2 / User3 / Legacy
			- SFD length / 8 / 4 / 8 / 16 / 32 / 8 / 16 / 64 / 8
		Using indices SFD_5, SFD_6 and SFD_7 requires [:SOURce<hw>]:BB:HUWB:SFD:USRState 1. \n
			:return: sfd_index: SFD_0| SFD_1| SFD_2| SFD_3| SFD_4| SFD_5| SFD_6| SFD_7| SFD_8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:SFD?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbSfdIndex)

	def set_value(self, sfd_index: enums.HrpUwbSfdIndex) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:SFD \n
		Snippet: driver.source.bb.huwb.sfd.set_value(sfd_index = enums.HrpUwbSfdIndex.SFD_0) \n
		Sets the start-of-frame delimiter (SFD) symbol sequence. The indices represent SFD symbol sequences with SFD lengths as
		listed in Table 'SFD: indices and lengths'. SFD: indices and lengths
			Table Header:  \n
			- Index / SFD_0 / SFD_1 / SFD_2 / SFD_3 / SFD_4 / SFD_5 / SFD_6 / SFD_7 / SFD_8
			- SFD / 0 / 1 / 2 / 3 / 4 / User1 / User2 / User3 / Legacy
			- SFD length / 8 / 4 / 8 / 16 / 32 / 8 / 16 / 64 / 8
		Using indices SFD_5, SFD_6 and SFD_7 requires [:SOURce<hw>]:BB:HUWB:SFD:USRState 1. \n
			:param sfd_index: SFD_0| SFD_1| SFD_2| SFD_3| SFD_4| SFD_5| SFD_6| SFD_7| SFD_8
		"""
		param = Conversions.enum_scalar_to_str(sfd_index, enums.HrpUwbSfdIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:SFD {param}')
