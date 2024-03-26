from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CelvCls:
	"""Celv commands group definition. 5 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: CeLevel, default value after init: CeLevel.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("celv", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_ceLevel_get', 'repcap_ceLevel_set', repcap.CeLevel.Nr0)

	def repcap_ceLevel_set(self, ceLevel: repcap.CeLevel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CeLevel.Default
		Default value after init: CeLevel.Nr0"""
		self._cmd_group.set_repcap_enum_value(ceLevel)

	def repcap_ceLevel_get(self) -> repcap.CeLevel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Config import ConfigCls
			self._config = ConfigCls(self._core, self._cmd_group)
		return self._config

	@property
	def foffset(self):
		"""foffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_foffset'):
			from .Foffset import FoffsetCls
			self._foffset = FoffsetCls(self._core, self._cmd_group)
		return self._foffset

	@property
	def hopping(self):
		"""hopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopping'):
			from .Hopping import HoppingCls
			self._hopping = HoppingCls(self._core, self._cmd_group)
		return self._hopping

	@property
	def repetit(self):
		"""repetit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetit'):
			from .Repetit import RepetitCls
			self._repetit = RepetitCls(self._core, self._cmd_group)
		return self._repetit

	@property
	def ssfPeriod(self):
		"""ssfPeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssfPeriod'):
			from .SsfPeriod import SsfPeriodCls
			self._ssfPeriod = SsfPeriodCls(self._core, self._cmd_group)
		return self._ssfPeriod

	def clone(self) -> 'CelvCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CelvCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
