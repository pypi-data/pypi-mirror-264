from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal.RepeatedCapability import RepeatedCapability
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TdmlCls:
	"""Tdml commands group definition. 6 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: ListIndexNull, default value after init: ListIndexNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tdml", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_listIndexNull_get', 'repcap_listIndexNull_set', repcap.ListIndexNull.Nr0)

	def repcap_listIndexNull_set(self, listIndexNull: repcap.ListIndexNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ListIndexNull.Default
		Default value after init: ListIndexNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(listIndexNull)

	def repcap_listIndexNull_get(self) -> repcap.ListIndexNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def td(self):
		"""td commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_td'):
			from .Td import TdCls
			self._td = TdCls(self._core, self._cmd_group)
		return self._td

	@property
	def tdaNum(self):
		"""tdaNum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdaNum'):
			from .TdaNum import TdaNumCls
			self._tdaNum = TdaNumCls(self._core, self._cmd_group)
		return self._tdaNum

	def clone(self) -> 'TdmlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TdmlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
