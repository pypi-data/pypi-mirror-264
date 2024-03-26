from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdGenerationCls:
	"""AdGeneration commands group definition. 102 total commands, 9 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("adGeneration", core, parent)

	@property
	def acquisition(self):
		"""acquisition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acquisition'):
			from .Acquisition import AcquisitionCls
			self._acquisition = AcquisitionCls(self._core, self._cmd_group)
		return self._acquisition

	@property
	def almanac(self):
		"""almanac commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_almanac'):
			from .Almanac import AlmanacCls
			self._almanac = AlmanacCls(self._core, self._cmd_group)
		return self._almanac

	@property
	def beidou(self):
		"""beidou commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Beidou import BeidouCls
			self._beidou = BeidouCls(self._core, self._cmd_group)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .Glonass import GlonassCls
			self._glonass = GlonassCls(self._core, self._cmd_group)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Gps import GpsCls
			self._gps = GpsCls(self._core, self._cmd_group)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Navic import NavicCls
			self._navic = NavicCls(self._core, self._cmd_group)
		return self._navic

	@property
	def navigation(self):
		"""navigation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_navigation'):
			from .Navigation import NavigationCls
			self._navigation = NavigationCls(self._core, self._cmd_group)
		return self._navigation

	@property
	def qzss(self):
		"""qzss commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Qzss import QzssCls
			self._qzss = QzssCls(self._core, self._cmd_group)
		return self._qzss

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.Hybrid:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:MODE \n
		Snippet: value: enums.Hybrid = driver.source.bb.gnss.adGeneration.get_mode() \n
		Defines the type of assistance data to be loaded. \n
			:return: mode: GPS| GALileo| GLONass| NAVic| QZSS| SBAS| BEIDou
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Hybrid)

	def set_mode(self, mode: enums.Hybrid) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:MODE \n
		Snippet: driver.source.bb.gnss.adGeneration.set_mode(mode = enums.Hybrid.BEIDou) \n
		Defines the type of assistance data to be loaded. \n
			:param mode: GPS| GALileo| GLONass| NAVic| QZSS| SBAS| BEIDou
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.Hybrid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:MODE {param}')

	def clone(self) -> 'AdGenerationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AdGenerationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
