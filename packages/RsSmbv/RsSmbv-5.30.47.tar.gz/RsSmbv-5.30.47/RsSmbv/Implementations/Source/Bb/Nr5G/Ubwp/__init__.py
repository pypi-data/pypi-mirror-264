from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UbwpCls:
	"""Ubwp commands group definition. 445 total commands, 2 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ubwp", core, parent)

	@property
	def restart(self):
		"""restart commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_restart'):
			from .Restart import RestartCls
			self._restart = RestartCls(self._core, self._cmd_group)
		return self._restart

	@property
	def user(self):
		"""user commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def get_nuser(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:NUSer \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.get_nuser() \n
		Sets the number of simulated users. \n
			:return: num_users: integer Range: 1 to 50
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:NUSer?')
		return Conversions.str_to_int(response)

	def set_nuser(self, num_users: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:NUSer \n
		Snippet: driver.source.bb.nr5G.ubwp.set_nuser(num_users = 1) \n
		Sets the number of simulated users. \n
			:param num_users: integer Range: 1 to 50
		"""
		param = Conversions.decimal_value_to_str(num_users)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:NUSer {param}')

	def get_sinterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:SINTerval \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.get_sinterval() \n
		Defines the number of slots after which the data source restarts (restart every <x> slots) .
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Single numerology setup
			- [:SOURce<hw>]:BB:NR5G:UBWP:RESTart = SLOT \n
			:return: slot_interval: integer Range: 1 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:SINTerval?')
		return Conversions.str_to_int(response)

	def set_sinterval(self, slot_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:SINTerval \n
		Snippet: driver.source.bb.nr5G.ubwp.set_sinterval(slot_interval = 1) \n
		Defines the number of slots after which the data source restarts (restart every <x> slots) .
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Single numerology setup
			- [:SOURce<hw>]:BB:NR5G:UBWP:RESTart = SLOT \n
			:param slot_interval: integer Range: 1 to 20
		"""
		param = Conversions.decimal_value_to_str(slot_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:SINTerval {param}')

	def get_soffset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:SOFFset \n
		Snippet: value: int = driver.source.bb.nr5G.ubwp.get_soffset() \n
		Defines an offset in terms of slots for the restart of the data source.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Single numerology setup
			- [:SOURce<hw>]:BB:NR5G:UBWP:RESTart = SLOT
			- [:SOURce<hw>]:BB:NR5G:UBWP:SINTerval > 1 \n
			:return: slot_offset: integer Maximum offset = slot interval - 1 Range: 0 to 19
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:SOFFset?')
		return Conversions.str_to_int(response)

	def set_soffset(self, slot_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:SOFFset \n
		Snippet: driver.source.bb.nr5G.ubwp.set_soffset(slot_offset = 1) \n
		Defines an offset in terms of slots for the restart of the data source.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Single numerology setup
			- [:SOURce<hw>]:BB:NR5G:UBWP:RESTart = SLOT
			- [:SOURce<hw>]:BB:NR5G:UBWP:SINTerval > 1 \n
			:param slot_offset: integer Maximum offset = slot interval - 1 Range: 0 to 19
		"""
		param = Conversions.decimal_value_to_str(slot_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:SOFFset {param}')

	def clone(self) -> 'UbwpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UbwpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
