from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpAddressCls:
	"""IpAddress commands group definition. 5 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ipAddress", core, parent)

	@property
	def subnet(self):
		"""subnet commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subnet'):
			from .Subnet import SubnetCls
			self._subnet = SubnetCls(self._core, self._cmd_group)
		return self._subnet

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EthernetMode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:MODE \n
		Snippet: value: enums.EthernetMode = driver.source.bb.nr5G.hfb.ethernet.ipAddress.get_mode() \n
		No command help available \n
			:return: eth_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EthernetMode)

	def set_mode(self, eth_mode: enums.EthernetMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:MODE \n
		Snippet: driver.source.bb.nr5G.hfb.ethernet.ipAddress.set_mode(eth_mode = enums.EthernetMode.AUTO) \n
		No command help available \n
			:param eth_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(eth_mode, enums.EthernetMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:MODE {param}')

	def get_port(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:PORT \n
		Snippet: value: int = driver.source.bb.nr5G.hfb.ethernet.ipAddress.get_port() \n
		No command help available \n
			:return: eth_port: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, eth_port: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:PORT \n
		Snippet: driver.source.bb.nr5G.hfb.ethernet.ipAddress.set_port(eth_port = 1) \n
		No command help available \n
			:param eth_port: No help available
		"""
		param = Conversions.decimal_value_to_str(eth_port)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:PORT {param}')

	# noinspection PyTypeChecker
	def get_protocol(self) -> enums.Nr5GethnertProtocol:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:PROTocol \n
		Snippet: value: enums.Nr5GethnertProtocol = driver.source.bb.nr5G.hfb.ethernet.ipAddress.get_protocol() \n
		No command help available \n
			:return: eth_protocol: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:PROTocol?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5GethnertProtocol)

	def set_protocol(self, eth_protocol: enums.Nr5GethnertProtocol) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:PROTocol \n
		Snippet: driver.source.bb.nr5G.hfb.ethernet.ipAddress.set_protocol(eth_protocol = enums.Nr5GethnertProtocol.TCP) \n
		No command help available \n
			:param eth_protocol: No help available
		"""
		param = Conversions.enum_scalar_to_str(eth_protocol, enums.Nr5GethnertProtocol)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:PROTocol {param}')

	def get_value(self) -> bytes:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress \n
		Snippet: value: bytes = driver.source.bb.nr5G.hfb.ethernet.ipAddress.get_value() \n
		No command help available \n
			:return: nr_5_gethernet_ip_address: No help available
		"""
		response = self._core.io.query_bin_block('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress?')
		return response

	def set_value(self, nr_5_gethernet_ip_address: bytes) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress \n
		Snippet: driver.source.bb.nr5G.hfb.ethernet.ipAddress.set_value(nr_5_gethernet_ip_address = b'ABCDEFGH') \n
		No command help available \n
			:param nr_5_gethernet_ip_address: No help available
		"""
		self._core.io.write_bin_block('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress ', nr_5_gethernet_ip_address)

	def clone(self) -> 'IpAddressCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IpAddressCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
