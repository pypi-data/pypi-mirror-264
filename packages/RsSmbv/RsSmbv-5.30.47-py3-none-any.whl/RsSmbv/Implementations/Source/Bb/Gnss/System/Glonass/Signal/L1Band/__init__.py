from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1BandCls:
	"""L1Band commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("l1Band", core, parent)

	@property
	def ca(self):
		"""ca commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ca'):
			from .Ca import CaCls
			self._ca = CaCls(self._core, self._cmd_group)
		return self._ca

	@property
	def l1Cdma(self):
		"""l1Cdma commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1Cdma'):
			from .L1Cdma import L1CdmaCls
			self._l1Cdma = L1CdmaCls(self._core, self._cmd_group)
		return self._l1Cdma

	def clone(self) -> 'L1BandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L1BandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
