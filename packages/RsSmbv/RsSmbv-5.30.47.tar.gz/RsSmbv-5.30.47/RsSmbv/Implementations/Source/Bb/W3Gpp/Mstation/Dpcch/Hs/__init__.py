from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HsCls:
	"""Hs commands group definition. 45 total commands, 20 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hs", core, parent)

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .Ccode import CcodeCls
			self._ccode = CcodeCls(self._core, self._cmd_group)
		return self._ccode

	@property
	def compatibility(self):
		"""compatibility commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_compatibility'):
			from .Compatibility import CompatibilityCls
			self._compatibility = CompatibilityCls(self._core, self._cmd_group)
		return self._compatibility

	@property
	def cqi(self):
		"""cqi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cqi'):
			from .Cqi import CqiCls
			self._cqi = CqiCls(self._core, self._cmd_group)
		return self._cqi

	@property
	def hack(self):
		"""hack commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_hack'):
			from .Hack import HackCls
			self._hack = HackCls(self._core, self._cmd_group)
		return self._hack

	@property
	def haPattern(self):
		"""haPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_haPattern'):
			from .HaPattern import HaPatternCls
			self._haPattern = HaPatternCls(self._core, self._cmd_group)
		return self._haPattern

	@property
	def mimo(self):
		"""mimo commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_mimo'):
			from .Mimo import MimoCls
			self._mimo = MimoCls(self._core, self._cmd_group)
		return self._mimo

	@property
	def mmode(self):
		"""mmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmode'):
			from .Mmode import MmodeCls
			self._mmode = MmodeCls(self._core, self._cmd_group)
		return self._mmode

	@property
	def pcqi(self):
		"""pcqi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcqi'):
			from .Pcqi import PcqiCls
			self._pcqi = PcqiCls(self._core, self._cmd_group)
		return self._pcqi

	@property
	def poAck(self):
		"""poAck commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poAck'):
			from .PoAck import PoAckCls
			self._poAck = PoAckCls(self._core, self._cmd_group)
		return self._poAck

	@property
	def poNack(self):
		"""poNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poNack'):
			from .PoNack import PoNackCls
			self._poNack = PoNackCls(self._core, self._cmd_group)
		return self._poNack

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def row(self):
		"""row commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	@property
	def rowCount(self):
		"""rowCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rowCount'):
			from .RowCount import RowCountCls
			self._rowCount = RowCountCls(self._core, self._cmd_group)
		return self._rowCount

	@property
	def sc(self):
		"""sc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sc'):
			from .Sc import ScCls
			self._sc = ScCls(self._core, self._cmd_group)
		return self._sc

	@property
	def scActive(self):
		"""scActive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scActive'):
			from .ScActive import ScActiveCls
			self._scActive = ScActiveCls(self._core, self._cmd_group)
		return self._scActive

	@property
	def sdelay(self):
		"""sdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sdelay'):
			from .Sdelay import SdelayCls
			self._sdelay = SdelayCls(self._core, self._cmd_group)
		return self._sdelay

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Sformat import SformatCls
			self._sformat = SformatCls(self._core, self._cmd_group)
		return self._sformat

	@property
	def slength(self):
		"""slength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Slength import SlengthCls
			self._slength = SlengthCls(self._core, self._cmd_group)
		return self._slength

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def ttiDistance(self):
		"""ttiDistance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiDistance'):
			from .TtiDistance import TtiDistanceCls
			self._ttiDistance = TtiDistanceCls(self._core, self._cmd_group)
		return self._ttiDistance

	def clone(self) -> 'HsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
