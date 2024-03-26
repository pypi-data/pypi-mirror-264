from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TransCls:
	"""Trans commands group definition. 23 total commands, 13 Subgroups, 0 group commands
	Repeated Capability: Transmission, default value after init: Transmission.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trans", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_transmission_get', 'repcap_transmission_set', repcap.Transmission.Nr1)

	def repcap_transmission_set(self, transmission: repcap.Transmission) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Transmission.Default
		Default value after init: Transmission.Nr1"""
		self._cmd_group.set_repcap_enum_value(transmission)

	def repcap_transmission_get(self) -> repcap.Transmission:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def harq(self):
		"""harq commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Harq import HarqCls
			self._harq = HarqCls(self._core, self._cmd_group)
		return self._harq

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def nrUnits(self):
		"""nrUnits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrUnits'):
			from .NrUnits import NrUnitsCls
			self._nrUnits = NrUnitsCls(self._core, self._cmd_group)
		return self._nrUnits

	@property
	def nscarriers(self):
		"""nscarriers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nscarriers'):
			from .Nscarriers import NscarriersCls
			self._nscarriers = NscarriersCls(self._core, self._cmd_group)
		return self._nscarriers

	@property
	def nslts(self):
		"""nslts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nslts'):
			from .Nslts import NsltsCls
			self._nslts = NsltsCls(self._core, self._cmd_group)
		return self._nslts

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def pusch(self):
		"""pusch commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetitions'):
			from .Repetitions import RepetitionsCls
			self._repetitions = RepetitionsCls(self._core, self._cmd_group)
		return self._repetitions

	@property
	def sirf(self):
		"""sirf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sirf'):
			from .Sirf import SirfCls
			self._sirf = SirfCls(self._core, self._cmd_group)
		return self._sirf

	@property
	def stsCarrier(self):
		"""stsCarrier commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsCarrier'):
			from .StsCarrier import StsCarrierCls
			self._stsCarrier = StsCarrierCls(self._core, self._cmd_group)
		return self._stsCarrier

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .StsFrame import StsFrameCls
			self._stsFrame = StsFrameCls(self._core, self._cmd_group)
		return self._stsFrame

	@property
	def stslot(self):
		"""stslot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stslot'):
			from .Stslot import StslotCls
			self._stslot = StslotCls(self._core, self._cmd_group)
		return self._stslot

	def clone(self) -> 'TransCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TransCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
