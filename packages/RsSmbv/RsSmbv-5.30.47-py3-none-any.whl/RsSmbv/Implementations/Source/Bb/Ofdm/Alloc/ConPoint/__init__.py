from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConPointCls:
	"""ConPoint commands group definition. 4 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: ConstelationPointNull, default value after init: ConstelationPointNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("conPoint", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_constelationPointNull_get', 'repcap_constelationPointNull_set', repcap.ConstelationPointNull.Nr0)

	def repcap_constelationPointNull_set(self, constelationPointNull: repcap.ConstelationPointNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ConstelationPointNull.Default
		Default value after init: ConstelationPointNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(constelationPointNull)

	def repcap_constelationPointNull_get(self) -> repcap.ConstelationPointNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def imag(self):
		"""imag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imag'):
			from .Imag import ImagCls
			self._imag = ImagCls(self._core, self._cmd_group)
		return self._imag

	@property
	def magn(self):
		"""magn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_magn'):
			from .Magn import MagnCls
			self._magn = MagnCls(self._core, self._cmd_group)
		return self._magn

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def real(self):
		"""real commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_real'):
			from .Real import RealCls
			self._real = RealCls(self._core, self._cmd_group)
		return self._real

	def clone(self) -> 'ConPointCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConPointCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
