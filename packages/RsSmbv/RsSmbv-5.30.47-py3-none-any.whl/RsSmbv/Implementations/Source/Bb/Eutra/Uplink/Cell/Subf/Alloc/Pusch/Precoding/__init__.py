from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrecodingCls:
	"""Precoding commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("precoding", core, parent)

	@property
	def cbIndex(self):
		"""cbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbIndex'):
			from .CbIndex import CbIndexCls
			self._cbIndex = CbIndexCls(self._core, self._cmd_group)
		return self._cbIndex

	@property
	def napUsed(self):
		"""napUsed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_napUsed'):
			from .NapUsed import NapUsedCls
			self._napUsed = NapUsedCls(self._core, self._cmd_group)
		return self._napUsed

	@property
	def noLayers(self):
		"""noLayers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noLayers'):
			from .NoLayers import NoLayersCls
			self._noLayers = NoLayersCls(self._core, self._cmd_group)
		return self._noLayers

	@property
	def scheme(self):
		"""scheme commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scheme'):
			from .Scheme import SchemeCls
			self._scheme = SchemeCls(self._core, self._cmd_group)
		return self._scheme

	def clone(self) -> 'PrecodingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PrecodingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
