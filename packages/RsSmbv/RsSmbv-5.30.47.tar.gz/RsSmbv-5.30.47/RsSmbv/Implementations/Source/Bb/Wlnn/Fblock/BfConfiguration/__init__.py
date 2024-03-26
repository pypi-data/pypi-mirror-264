from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BfConfigurationCls:
	"""BfConfiguration commands group definition. 27 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bfConfiguration", core, parent)

	@property
	def binterval(self):
		"""binterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_binterval'):
			from .Binterval import BintervalCls
			self._binterval = BintervalCls(self._core, self._cmd_group)
		return self._binterval

	@property
	def capability(self):
		"""capability commands group. 16 Sub-classes, 0 commands."""
		if not hasattr(self, '_capability'):
			from .Capability import CapabilityCls
			self._capability = CapabilityCls(self._core, self._cmd_group)
		return self._capability

	@property
	def dcChannel(self):
		"""dcChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcChannel'):
			from .DcChannel import DcChannelCls
			self._dcChannel = DcChannelCls(self._core, self._cmd_group)
		return self._dcChannel

	@property
	def erp(self):
		"""erp commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_erp'):
			from .Erp import ErpCls
			self._erp = ErpCls(self._core, self._cmd_group)
		return self._erp

	@property
	def htCapability(self):
		"""htCapability commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_htCapability'):
			from .HtCapability import HtCapabilityCls
			self._htCapability = HtCapabilityCls(self._core, self._cmd_group)
		return self._htCapability

	@property
	def iaWindow(self):
		"""iaWindow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iaWindow'):
			from .IaWindow import IaWindowCls
			self._iaWindow = IaWindowCls(self._core, self._cmd_group)
		return self._iaWindow

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def ssid(self):
		"""ssid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssid'):
			from .Ssid import SsidCls
			self._ssid = SsidCls(self._core, self._cmd_group)
		return self._ssid

	@property
	def tstamp(self):
		"""tstamp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tstamp'):
			from .Tstamp import TstampCls
			self._tstamp = TstampCls(self._core, self._cmd_group)
		return self._tstamp

	def clone(self) -> 'BfConfigurationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BfConfigurationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
