from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrecodingCls:
	"""Precoding commands group definition. 11 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("precoding", core, parent)

	@property
	def ap(self):
		"""ap commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ap'):
			from .Ap import ApCls
			self._ap = ApCls(self._core, self._cmd_group)
		return self._ap

	@property
	def apm(self):
		"""apm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apm'):
			from .Apm import ApmCls
			self._apm = ApmCls(self._core, self._cmd_group)
		return self._apm

	@property
	def cbIndex(self):
		"""cbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbIndex'):
			from .CbIndex import CbIndexCls
			self._cbIndex = CbIndexCls(self._core, self._cmd_group)
		return self._cbIndex

	@property
	def ccd(self):
		"""ccd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccd'):
			from .Ccd import CcdCls
			self._ccd = CcdCls(self._core, self._cmd_group)
		return self._ccd

	@property
	def daFormat(self):
		"""daFormat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_daFormat'):
			from .DaFormat import DaFormatCls
			self._daFormat = DaFormatCls(self._core, self._cmd_group)
		return self._daFormat

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

	@property
	def scid(self):
		"""scid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scid'):
			from .Scid import ScidCls
			self._scid = ScidCls(self._core, self._cmd_group)
		return self._scid

	@property
	def trScheme(self):
		"""trScheme commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trScheme'):
			from .TrScheme import TrSchemeCls
			self._trScheme = TrSchemeCls(self._core, self._cmd_group)
		return self._trScheme

	def clone(self) -> 'PrecodingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PrecodingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
