from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SconfigurationCls:
	"""Sconfiguration commands group definition. 158 total commands, 6 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sconfiguration", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	@property
	def baseband(self):
		"""baseband commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_baseband'):
			from .Baseband import BasebandCls
			self._baseband = BasebandCls(self._core, self._cmd_group)
		return self._baseband

	@property
	def diq(self):
		"""diq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_diq'):
			from .Diq import DiqCls
			self._diq = DiqCls(self._core, self._cmd_group)
		return self._diq

	@property
	def external(self):
		"""external commands group. 8 Sub-classes, 3 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	@property
	def multiInstrument(self):
		"""multiInstrument commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_multiInstrument'):
			from .MultiInstrument import MultiInstrumentCls
			self._multiInstrument = MultiInstrumentCls(self._core, self._cmd_group)
		return self._multiInstrument

	@property
	def output(self):
		"""output commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	def preset(self) -> None:
		"""SCPI: SCONfiguration:PRESet \n
		Snippet: driver.sconfiguration.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SCONfiguration:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SCONfiguration:PRESet \n
		Snippet: driver.sconfiguration.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SCONfiguration:PRESet', opc_timeout_ms)

	def clone(self) -> 'SconfigurationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SconfigurationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
