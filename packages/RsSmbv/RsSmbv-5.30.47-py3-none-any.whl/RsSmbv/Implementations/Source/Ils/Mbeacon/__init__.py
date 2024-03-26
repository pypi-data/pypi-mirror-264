from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MbeaconCls:
	"""Mbeacon commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mbeacon", core, parent)

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:PRESet \n
		Snippet: driver.source.ils.mbeacon.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:PRESet \n
		Snippet: driver.source.ils.mbeacon.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:MBEacon:PRESet', opc_timeout_ms)

	def clone(self) -> 'MbeaconCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MbeaconCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
