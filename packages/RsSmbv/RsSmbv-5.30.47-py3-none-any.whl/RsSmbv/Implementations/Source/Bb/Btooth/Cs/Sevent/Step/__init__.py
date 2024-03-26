from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StepCls:
	"""Step commands group definition. 6 total commands, 6 Subgroups, 0 group commands
	Repeated Capability: StepNull, default value after init: StepNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("step", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_stepNull_get', 'repcap_stepNull_set', repcap.StepNull.Nr0)

	def repcap_stepNull_set(self, stepNull: repcap.StepNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to StepNull.Default
		Default value after init: StepNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(stepNull)

	def repcap_stepNull_get(self) -> repcap.StepNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def caAddress(self):
		"""caAddress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caAddress'):
			from .CaAddress import CaAddressCls
			self._caAddress = CaAddressCls(self._core, self._cmd_group)
		return self._caAddress

	@property
	def cindex(self):
		"""cindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cindex'):
			from .Cindex import CindexCls
			self._cindex = CindexCls(self._core, self._cmd_group)
		return self._cindex

	@property
	def csignal(self):
		"""csignal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csignal'):
			from .Csignal import CsignalCls
			self._csignal = CsignalCls(self._core, self._cmd_group)
		return self._csignal

	@property
	def ctExtension(self):
		"""ctExtension commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctExtension'):
			from .CtExtension import CtExtensionCls
			self._ctExtension = CtExtensionCls(self._core, self._cmd_group)
		return self._ctExtension

	@property
	def mtype(self):
		"""mtype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtype'):
			from .Mtype import MtypeCls
			self._mtype = MtypeCls(self._core, self._cmd_group)
		return self._mtype

	@property
	def scontent(self):
		"""scontent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scontent'):
			from .Scontent import ScontentCls
			self._scontent = ScontentCls(self._core, self._cmd_group)
		return self._scontent

	def clone(self) -> 'StepCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StepCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
