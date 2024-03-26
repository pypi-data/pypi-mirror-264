from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EthernetCls:
	"""Ethernet commands group definition. 6 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ethernet", core, parent)

	@property
	def ipAddress(self):
		"""ipAddress commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_ipAddress'):
			from .IpAddress import IpAddressCls
			self._ipAddress = IpAddressCls(self._core, self._cmd_group)
		return self._ipAddress

	def get_hostname(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:HOSTname \n
		Snippet: value: str = driver.source.bb.nr5G.hfb.ethernet.get_hostname() \n
		No command help available \n
			:return: eth_hostname: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:HOSTname?')
		return trim_str_response(response)

	def clone(self) -> 'EthernetCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EthernetCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
