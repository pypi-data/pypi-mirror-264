from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CapabilityCls:
	"""Capability commands group definition. 16 total commands, 16 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("capability", core, parent)

	@property
	def apsd(self):
		"""apsd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apsd'):
			from .Apsd import ApsdCls
			self._apsd = ApsdCls(self._core, self._cmd_group)
		return self._apsd

	@property
	def cagility(self):
		"""cagility commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cagility'):
			from .Cagility import CagilityCls
			self._cagility = CagilityCls(self._core, self._cmd_group)
		return self._cagility

	@property
	def cpollable(self):
		"""cpollable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpollable'):
			from .Cpollable import CpollableCls
			self._cpollable = CpollableCls(self._core, self._cmd_group)
		return self._cpollable

	@property
	def cpRequest(self):
		"""cpRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpRequest'):
			from .CpRequest import CpRequestCls
			self._cpRequest = CpRequestCls(self._core, self._cmd_group)
		return self._cpRequest

	@property
	def dback(self):
		"""dback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dback'):
			from .Dback import DbackCls
			self._dback = DbackCls(self._core, self._cmd_group)
		return self._dback

	@property
	def dofdm(self):
		"""dofdm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dofdm'):
			from .Dofdm import DofdmCls
			self._dofdm = DofdmCls(self._core, self._cmd_group)
		return self._dofdm

	@property
	def ess(self):
		"""ess commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ess'):
			from .Ess import EssCls
			self._ess = EssCls(self._core, self._cmd_group)
		return self._ess

	@property
	def iback(self):
		"""iback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iback'):
			from .Iback import IbackCls
			self._iback = IbackCls(self._core, self._cmd_group)
		return self._iback

	@property
	def ibss(self):
		"""ibss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ibss'):
			from .Ibss import IbssCls
			self._ibss = IbssCls(self._core, self._cmd_group)
		return self._ibss

	@property
	def pbcc(self):
		"""pbcc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pbcc'):
			from .Pbcc import PbccCls
			self._pbcc = PbccCls(self._core, self._cmd_group)
		return self._pbcc

	@property
	def privacy(self):
		"""privacy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_privacy'):
			from .Privacy import PrivacyCls
			self._privacy = PrivacyCls(self._core, self._cmd_group)
		return self._privacy

	@property
	def qos(self):
		"""qos commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qos'):
			from .Qos import QosCls
			self._qos = QosCls(self._core, self._cmd_group)
		return self._qos

	@property
	def rmeasurement(self):
		"""rmeasurement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmeasurement'):
			from .Rmeasurement import RmeasurementCls
			self._rmeasurement = RmeasurementCls(self._core, self._cmd_group)
		return self._rmeasurement

	@property
	def smgmt(self):
		"""smgmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smgmt'):
			from .Smgmt import SmgmtCls
			self._smgmt = SmgmtCls(self._core, self._cmd_group)
		return self._smgmt

	@property
	def spreamble(self):
		"""spreamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spreamble'):
			from .Spreamble import SpreambleCls
			self._spreamble = SpreambleCls(self._core, self._cmd_group)
		return self._spreamble

	@property
	def ssTime(self):
		"""ssTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssTime'):
			from .SsTime import SsTimeCls
			self._ssTime = SsTimeCls(self._core, self._cmd_group)
		return self._ssTime

	def clone(self) -> 'CapabilityCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CapabilityCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
