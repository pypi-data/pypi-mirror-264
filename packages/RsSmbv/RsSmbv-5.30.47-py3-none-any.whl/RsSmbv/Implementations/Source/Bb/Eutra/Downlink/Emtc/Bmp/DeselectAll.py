from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeselectAllCls:
	"""DeselectAll commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: DeselectAll, default value after init: DeselectAll.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("deselectAll", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_deselectAll_get', 'repcap_deselectAll_set', repcap.DeselectAll.Nr0)

	def repcap_deselectAll_set(self, deselectAll: repcap.DeselectAll) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to DeselectAll.Default
		Default value after init: DeselectAll.Nr0"""
		self._cmd_group.set_repcap_enum_value(deselectAll)

	def repcap_deselectAll_get(self) -> repcap.DeselectAll:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, deselectAll=repcap.DeselectAll.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:DESelectall<ST> \n
		Snippet: driver.source.bb.eutra.downlink.emtc.bmp.deselectAll.set(deselectAll = repcap.DeselectAll.Default) \n
		Sets all SFs as valid or invalid. \n
			:param deselectAll: optional repeated capability selector. Default value: Nr0 (settable in the interface 'DeselectAll')
		"""
		deselectAll_cmd_val = self._cmd_group.get_repcap_cmd_value(deselectAll, repcap.DeselectAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:DESelectall{deselectAll_cmd_val}')

	def set_with_opc(self, deselectAll=repcap.DeselectAll.Default, opc_timeout_ms: int = -1) -> None:
		deselectAll_cmd_val = self._cmd_group.get_repcap_cmd_value(deselectAll, repcap.DeselectAll)
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:DESelectall<ST> \n
		Snippet: driver.source.bb.eutra.downlink.emtc.bmp.deselectAll.set_with_opc(deselectAll = repcap.DeselectAll.Default) \n
		Sets all SFs as valid or invalid. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param deselectAll: optional repeated capability selector. Default value: Nr0 (settable in the interface 'DeselectAll')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:DESelectall{deselectAll_cmd_val}', opc_timeout_ms)

	def clone(self) -> 'DeselectAllCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DeselectAllCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
