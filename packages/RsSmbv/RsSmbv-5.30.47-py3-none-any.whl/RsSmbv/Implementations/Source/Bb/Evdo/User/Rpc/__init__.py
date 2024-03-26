from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RpcCls:
	"""Rpc commands group definition. 5 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rpc", core, parent)

	@property
	def inject(self):
		"""inject commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inject'):
			from .Inject import InjectCls
			self._inject = InjectCls(self._core, self._cmd_group)
		return self._inject

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_range'):
			from .Range import RangeCls
			self._range = RangeCls(self._core, self._cmd_group)
		return self._range

	@property
	def zone(self):
		"""zone commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_zone'):
			from .Zone import ZoneCls
			self._zone = ZoneCls(self._core, self._cmd_group)
		return self._zone

	def clone(self) -> 'RpcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RpcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
