from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QzssCls:
	"""Qzss commands group definition. 223 total commands, 13 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("qzss", core, parent)

	@property
	def healthy(self):
		"""healthy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_healthy'):
			from .Healthy import HealthyCls
			self._healthy = HealthyCls(self._core, self._cmd_group)
		return self._healthy

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def mcontrol(self):
		"""mcontrol commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mcontrol'):
			from .Mcontrol import McontrolCls
			self._mcontrol = McontrolCls(self._core, self._cmd_group)
		return self._mcontrol

	@property
	def mpath(self):
		"""mpath commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mpath'):
			from .Mpath import MpathCls
			self._mpath = MpathCls(self._core, self._cmd_group)
		return self._mpath

	@property
	def nmessage(self):
		"""nmessage commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmessage'):
			from .Nmessage import NmessageCls
			self._nmessage = NmessageCls(self._core, self._cmd_group)
		return self._nmessage

	@property
	def power(self):
		"""power commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def prErrors(self):
		"""prErrors commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_prErrors'):
			from .PrErrors import PrErrorsCls
			self._prErrors = PrErrorsCls(self._core, self._cmd_group)
		return self._prErrors

	@property
	def present(self):
		"""present commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_present'):
			from .Present import PresentCls
			self._present = PresentCls(self._core, self._cmd_group)
		return self._present

	@property
	def sdynamics(self):
		"""sdynamics commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_sdynamics'):
			from .Sdynamics import SdynamicsCls
			self._sdynamics = SdynamicsCls(self._core, self._cmd_group)
		return self._sdynamics

	@property
	def signal(self):
		"""signal commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_signal'):
			from .Signal import SignalCls
			self._signal = SignalCls(self._core, self._cmd_group)
		return self._signal

	@property
	def simulated(self):
		"""simulated commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_simulated'):
			from .Simulated import SimulatedCls
			self._simulated = SimulatedCls(self._core, self._cmd_group)
		return self._simulated

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def visibility(self):
		"""visibility commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_visibility'):
			from .Visibility import VisibilityCls
			self._visibility = VisibilityCls(self._core, self._cmd_group)
		return self._visibility

	def clone(self) -> 'QzssCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = QzssCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
