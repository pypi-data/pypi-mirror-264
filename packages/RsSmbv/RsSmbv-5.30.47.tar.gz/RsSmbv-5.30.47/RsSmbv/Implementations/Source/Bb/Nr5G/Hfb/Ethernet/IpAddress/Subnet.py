from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubnetCls:
	"""Subnet commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subnet", core, parent)

	def get_mask(self) -> bytes:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:SUBNet:MASK \n
		Snippet: value: bytes = driver.source.bb.nr5G.hfb.ethernet.ipAddress.subnet.get_mask() \n
		No command help available \n
			:return: nr_5_gethernet_sub_net_mask: No help available
		"""
		response = self._core.io.query_bin_block('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:SUBNet:MASK?')
		return response

	def set_mask(self, nr_5_gethernet_sub_net_mask: bytes) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:HFB:ETHernet:IPADdress:SUBNet:MASK \n
		Snippet: driver.source.bb.nr5G.hfb.ethernet.ipAddress.subnet.set_mask(nr_5_gethernet_sub_net_mask = b'ABCDEFGH') \n
		No command help available \n
			:param nr_5_gethernet_sub_net_mask: No help available
		"""
		self._core.io.write_bin_block('SOURce<HwInstance>:BB:NR5G:HFB:ETHernet:IPADdress:SUBNet:MASK ', nr_5_gethernet_sub_net_mask)
