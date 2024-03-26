from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EditCls:
	"""Edit commands group definition. 7 total commands, 3 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("edit", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Device import DeviceCls
			self._device = DeviceCls(self._core, self._cmd_group)
		return self._device

	@property
	def remove(self):
		"""remove commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_remove'):
			from .Remove import RemoveCls
			self._remove = RemoveCls(self._core, self._cmd_group)
		return self._remove

	def get_alias(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:ALIas \n
		Snippet: value: str = driver.source.areGenerator.external.remote.edit.get_alias() \n
		No command help available \n
			:return: symbolic_name: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:ALIas?')
		return trim_str_response(response)

	def set_alias(self, symbolic_name: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:ALIas \n
		Snippet: driver.source.areGenerator.external.remote.edit.set_alias(symbolic_name = 'abc') \n
		No command help available \n
			:param symbolic_name: No help available
		"""
		param = Conversions.value_to_quoted_str(symbolic_name)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:ALIas {param}')

	def get_hostname(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:HOSTname \n
		Snippet: value: str = driver.source.areGenerator.external.remote.edit.get_hostname() \n
		No command help available \n
			:return: hostname_or_ip: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, hostname_or_ip: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:HOSTname \n
		Snippet: driver.source.areGenerator.external.remote.edit.set_hostname(hostname_or_ip = 'abc') \n
		No command help available \n
			:param hostname_or_ip: No help available
		"""
		param = Conversions.value_to_quoted_str(hostname_or_ip)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:HOSTname {param}')

	def get_iselect(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:ISELect \n
		Snippet: value: str = driver.source.areGenerator.external.remote.edit.get_iselect() \n
		No command help available \n
			:return: instrument_name: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:ISELect?')
		return trim_str_response(response)

	def set_iselect(self, instrument_name: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:ISELect \n
		Snippet: driver.source.areGenerator.external.remote.edit.set_iselect(instrument_name = 'abc') \n
		No command help available \n
			:param instrument_name: No help available
		"""
		param = Conversions.value_to_quoted_str(instrument_name)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:ISELect {param}')

	# noinspection PyTypeChecker
	def get_rchannel(self) -> enums.RcConnType:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:RCHannel \n
		Snippet: value: enums.RcConnType = driver.source.areGenerator.external.remote.edit.get_rchannel() \n
		No command help available \n
			:return: remote_channel: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:RCHannel?')
		return Conversions.str_to_scalar_enum(response, enums.RcConnType)

	def set_rchannel(self, remote_channel: enums.RcConnType) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:EXTernal:REMote:EDIT:RCHannel \n
		Snippet: driver.source.areGenerator.external.remote.edit.set_rchannel(remote_channel = enums.RcConnType.FRONtend) \n
		No command help available \n
			:param remote_channel: No help available
		"""
		param = Conversions.enum_scalar_to_str(remote_channel, enums.RcConnType)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:EXTernal:REMote:EDIT:RCHannel {param}')

	def clone(self) -> 'EditCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EditCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
