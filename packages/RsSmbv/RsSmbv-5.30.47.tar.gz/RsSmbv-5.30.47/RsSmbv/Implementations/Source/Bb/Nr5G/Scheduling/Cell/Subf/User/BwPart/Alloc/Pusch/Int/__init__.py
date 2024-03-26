from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IntCls:
	"""Int commands group definition. 1 total commands, 1 Subgroups, 0 group commands
	Repeated Capability: InterlaceNull, default value after init: InterlaceNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("int", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_interlaceNull_get', 'repcap_interlaceNull_set', repcap.InterlaceNull.Nr0)

	def repcap_interlaceNull_set(self, interlaceNull: repcap.InterlaceNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to InterlaceNull.Default
		Default value after init: InterlaceNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(interlaceNull)

	def repcap_interlaceNull_get(self) -> repcap.InterlaceNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def intl(self):
		"""intl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_intl'):
			from .Intl import IntlCls
			self._intl = IntlCls(self._core, self._cmd_group)
		return self._intl

	def clone(self) -> 'IntCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IntCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
