from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SbasCls:
	"""Sbas commands group definition. 99 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sbas", core, parent)

	@property
	def egnos(self):
		"""egnos commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_egnos'):
			from .Egnos import EgnosCls
			self._egnos = EgnosCls(self._core, self._cmd_group)
		return self._egnos

	@property
	def gagan(self):
		"""gagan commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_gagan'):
			from .Gagan import GaganCls
			self._gagan = GaganCls(self._core, self._cmd_group)
		return self._gagan

	@property
	def msas(self):
		"""msas commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_msas'):
			from .Msas import MsasCls
			self._msas = MsasCls(self._core, self._cmd_group)
		return self._msas

	@property
	def signal(self):
		"""signal commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_signal'):
			from .Signal import SignalCls
			self._signal = SignalCls(self._core, self._cmd_group)
		return self._signal

	@property
	def waas(self):
		"""waas commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_waas'):
			from .Waas import WaasCls
			self._waas = WaasCls(self._core, self._cmd_group)
		return self._waas

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SYSTem:SBAS:[STATe] \n
		Snippet: value: bool = driver.source.bb.gnss.system.sbas.get_state() \n
		Queries if at least one of the SBAS system is enabled. \n
			:return: state: 1| ON| 0| OFF 1 At least one SBAS system is enabled. To enable each of the SBAS systems, use the corresponding command, e.g. [:SOURcehw]:BB:GNSS:SYSTem:SBAS:EGNOS[:STATe]. 0 All SBAS systems are disabled.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:STATe?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'SbasCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SbasCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
