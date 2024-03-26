from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpcbCls:
	"""Spcb commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spcb", core, parent)

	@property
	def i11(self):
		"""i11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i11'):
			from .I11 import I11Cls
			self._i11 = I11Cls(self._core, self._cmd_group)
		return self._i11

	@property
	def i12(self):
		"""i12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i12'):
			from .I12 import I12Cls
			self._i12 = I12Cls(self._core, self._cmd_group)
		return self._i12

	@property
	def i13(self):
		"""i13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i13'):
			from .I13 import I13Cls
			self._i13 = I13Cls(self._core, self._cmd_group)
		return self._i13

	@property
	def i2(self):
		"""i2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_i2'):
			from .I2 import I2Cls
			self._i2 = I2Cls(self._core, self._cmd_group)
		return self._i2

	def clone(self) -> 'SpcbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpcbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
