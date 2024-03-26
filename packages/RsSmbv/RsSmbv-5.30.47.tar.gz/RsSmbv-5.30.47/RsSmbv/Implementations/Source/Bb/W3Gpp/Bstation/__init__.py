from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BstationCls:
	"""Bstation commands group definition. 170 total commands, 13 Subgroups, 1 group commands
	Repeated Capability: BaseStation, default value after init: BaseStation.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bstation", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_baseStation_get', 'repcap_baseStation_set', repcap.BaseStation.Nr1)

	def repcap_baseStation_set(self, baseStation: repcap.BaseStation) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BaseStation.Default
		Default value after init: BaseStation.Nr1"""
		self._cmd_group.set_repcap_enum_value(baseStation)

	def repcap_baseStation_get(self) -> repcap.BaseStation:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def channel(self):
		"""channel commands group. 14 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def cmode(self):
		"""cmode commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmode'):
			from .Cmode import CmodeCls
			self._cmode = CmodeCls(self._core, self._cmd_group)
		return self._cmode

	@property
	def dconflict(self):
		"""dconflict commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dconflict'):
			from .Dconflict import DconflictCls
			self._dconflict = DconflictCls(self._core, self._cmd_group)
		return self._dconflict

	@property
	def enhanced(self):
		"""enhanced commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_enhanced'):
			from .Enhanced import EnhancedCls
			self._enhanced = EnhancedCls(self._core, self._cmd_group)
		return self._enhanced

	@property
	def ocns(self):
		"""ocns commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_ocns'):
			from .Ocns import OcnsCls
			self._ocns = OcnsCls(self._core, self._cmd_group)
		return self._ocns

	@property
	def oltDiversity(self):
		"""oltDiversity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oltDiversity'):
			from .OltDiversity import OltDiversityCls
			self._oltDiversity = OltDiversityCls(self._core, self._cmd_group)
		return self._oltDiversity

	@property
	def pindicator(self):
		"""pindicator commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pindicator'):
			from .Pindicator import PindicatorCls
			self._pindicator = PindicatorCls(self._core, self._cmd_group)
		return self._pindicator

	@property
	def scode(self):
		"""scode commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Scode import ScodeCls
			self._scode = ScodeCls(self._core, self._cmd_group)
		return self._scode

	@property
	def scpich(self):
		"""scpich commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scpich'):
			from .Scpich import ScpichCls
			self._scpich = ScpichCls(self._core, self._cmd_group)
		return self._scpich

	@property
	def sscg(self):
		"""sscg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sscg'):
			from .Sscg import SscgCls
			self._sscg = SscgCls(self._core, self._cmd_group)
		return self._sscg

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Tdelay import TdelayCls
			self._tdelay = TdelayCls(self._core, self._cmd_group)
		return self._tdelay

	@property
	def tdiversity(self):
		"""tdiversity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdiversity'):
			from .Tdiversity import TdiversityCls
			self._tdiversity = TdiversityCls(self._core, self._cmd_group)
		return self._tdiversity

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:PRESet \n
		Snippet: driver.source.bb.w3Gpp.bstation.preset() \n
		The command produces a standardized default for all the base stations. The settings correspond to the *RST values
		specified for the commands. All base station settings are preset. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:PRESet \n
		Snippet: driver.source.bb.w3Gpp.bstation.preset_with_opc() \n
		The command produces a standardized default for all the base stations. The settings correspond to the *RST values
		specified for the commands. All base station settings are preset. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation:PRESet', opc_timeout_ms)

	def clone(self) -> 'BstationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BstationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
