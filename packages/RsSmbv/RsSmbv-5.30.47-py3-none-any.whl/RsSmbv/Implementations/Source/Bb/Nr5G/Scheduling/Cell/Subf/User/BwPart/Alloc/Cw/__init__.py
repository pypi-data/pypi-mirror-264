from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal.RepeatedCapability import RepeatedCapability
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CwCls:
	"""Cw commands group definition. 25 total commands, 7 Subgroups, 0 group commands
	Repeated Capability: CodewordNull, default value after init: CodewordNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cw", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_codewordNull_get', 'repcap_codewordNull_set', repcap.CodewordNull.Nr0)

	def repcap_codewordNull_set(self, codewordNull: repcap.CodewordNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CodewordNull.Default
		Default value after init: CodewordNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(codewordNull)

	def repcap_codewordNull_get(self) -> repcap.CodewordNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cmod(self):
		"""cmod commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmod'):
			from .Cmod import CmodCls
			self._cmod = CmodCls(self._core, self._cmd_group)
		return self._cmod

	@property
	def mod(self):
		"""mod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mod'):
			from .Mod import ModCls
			self._mod = ModCls(self._core, self._cmd_group)
		return self._mod

	@property
	def pdsch(self):
		"""pdsch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdsch'):
			from .Pdsch import PdschCls
			self._pdsch = PdschCls(self._core, self._cmd_group)
		return self._pdsch

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .PhysBits import PhysBitsCls
			self._physBits = PhysBitsCls(self._core, self._cmd_group)
		return self._physBits

	@property
	def pssch(self):
		"""pssch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pssch'):
			from .Pssch import PsschCls
			self._pssch = PsschCls(self._core, self._cmd_group)
		return self._pssch

	@property
	def pusch(self):
		"""pusch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	@property
	def rmcStable(self):
		"""rmcStable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmcStable'):
			from .RmcStable import RmcStableCls
			self._rmcStable = RmcStableCls(self._core, self._cmd_group)
		return self._rmcStable

	def clone(self) -> 'CwCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CwCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
