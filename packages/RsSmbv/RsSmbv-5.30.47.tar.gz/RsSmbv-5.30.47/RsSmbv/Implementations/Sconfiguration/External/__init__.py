from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 141 total commands, 8 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	@property
	def bbmm(self):
		"""bbmm commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_bbmm'):
			from .Bbmm import BbmmCls
			self._bbmm = BbmmCls(self._core, self._cmd_group)
		return self._bbmm

	@property
	def coder(self):
		"""coder commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_coder'):
			from .Coder import CoderCls
			self._coder = CoderCls(self._core, self._cmd_group)
		return self._coder

	@property
	def digital(self):
		"""digital commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import DigitalCls
			self._digital = DigitalCls(self._core, self._cmd_group)
		return self._digital

	@property
	def fader(self):
		"""fader commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_fader'):
			from .Fader import FaderCls
			self._fader = FaderCls(self._core, self._cmd_group)
		return self._fader

	@property
	def hsDigital(self):
		"""hsDigital commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsDigital'):
			from .HsDigital import HsDigitalCls
			self._hsDigital = HsDigitalCls(self._core, self._cmd_group)
		return self._hsDigital

	@property
	def iqOutput(self):
		"""iqOutput commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOutput'):
			from .IqOutput import IqOutputCls
			self._iqOutput = IqOutputCls(self._core, self._cmd_group)
		return self._iqOutput

	@property
	def remote(self):
		"""remote commands group. 7 Sub-classes, 3 commands."""
		if not hasattr(self, '_remote'):
			from .Remote import RemoteCls
			self._remote = RemoteCls(self._core, self._cmd_group)
		return self._remote

	@property
	def rf(self):
		"""rf commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import RfCls
			self._rf = RfCls(self._core, self._cmd_group)
		return self._rf

	def get_aconnect(self) -> bool:
		"""SCPI: SCONfiguration:EXTernal:ACONnect \n
		Snippet: value: bool = driver.sconfiguration.external.get_aconnect() \n
		Enables automatic detection and connection setup of connected external instruments. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SCONfiguration:EXTernal:ACONnect?')
		return Conversions.str_to_bool(response)

	def set_aconnect(self, state: bool) -> None:
		"""SCPI: SCONfiguration:EXTernal:ACONnect \n
		Snippet: driver.sconfiguration.external.set_aconnect(state = False) \n
		Enables automatic detection and connection setup of connected external instruments. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SCONfiguration:EXTernal:ACONnect {param}')

	# noinspection PyTypeChecker
	def get_display(self) -> enums.ExtDevDisplay:
		"""SCPI: SCONfiguration:EXTernal:DISPlay \n
		Snippet: value: enums.ExtDevDisplay = driver.sconfiguration.external.get_display() \n
		Filters the displayed connectors upon the selected criteria. \n
			:return: display_mode: ALL| MAPPed| INPut| OUTPut
		"""
		response = self._core.io.query_str('SCONfiguration:EXTernal:DISPlay?')
		return Conversions.str_to_scalar_enum(response, enums.ExtDevDisplay)

	def set_display(self, display_mode: enums.ExtDevDisplay) -> None:
		"""SCPI: SCONfiguration:EXTernal:DISPlay \n
		Snippet: driver.sconfiguration.external.set_display(display_mode = enums.ExtDevDisplay.ALL) \n
		Filters the displayed connectors upon the selected criteria. \n
			:param display_mode: ALL| MAPPed| INPut| OUTPut
		"""
		param = Conversions.enum_scalar_to_str(display_mode, enums.ExtDevDisplay)
		self._core.io.write(f'SCONfiguration:EXTernal:DISPlay {param}')

	def get_pbehaviour(self) -> bool:
		"""SCPI: SCONfiguration:EXTernal:PBEHaviour \n
		Snippet: value: bool = driver.sconfiguration.external.get_pbehaviour() \n
		If enabled, the connection to the external instruments is retained after preset (*RST) of the instrument. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SCONfiguration:EXTernal:PBEHaviour?')
		return Conversions.str_to_bool(response)

	def set_pbehaviour(self, state: bool) -> None:
		"""SCPI: SCONfiguration:EXTernal:PBEHaviour \n
		Snippet: driver.sconfiguration.external.set_pbehaviour(state = False) \n
		If enabled, the connection to the external instruments is retained after preset (*RST) of the instrument. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SCONfiguration:EXTernal:PBEHaviour {param}')

	def clone(self) -> 'ExternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
