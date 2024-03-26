from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectionCls:
	"""Selection commands group definition. 33 total commands, 10 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("selection", core, parent)

	@property
	def beidou(self):
		"""beidou commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_beidou'):
			from .Beidou import BeidouCls
			self._beidou = BeidouCls(self._core, self._cmd_group)
		return self._beidou

	@property
	def channels(self):
		"""channels commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channels'):
			from .Channels import ChannelsCls
			self._channels = ChannelsCls(self._core, self._cmd_group)
		return self._channels

	@property
	def eobscuration(self):
		"""eobscuration commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_eobscuration'):
			from .Eobscuration import EobscurationCls
			self._eobscuration = EobscurationCls(self._core, self._cmd_group)
		return self._eobscuration

	@property
	def galileo(self):
		"""galileo commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_glonass'):
			from .Glonass import GlonassCls
			self._glonass = GlonassCls(self._core, self._cmd_group)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_gps'):
			from .Gps import GpsCls
			self._gps = GpsCls(self._core, self._cmd_group)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_navic'):
			from .Navic import NavicCls
			self._navic = NavicCls(self._core, self._cmd_group)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_qzss'):
			from .Qzss import QzssCls
			self._qzss = QzssCls(self._core, self._cmd_group)
		return self._qzss

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	@property
	def sbas(self):
		"""sbas commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_sbas'):
			from .Sbas import SbasCls
			self._sbas = SbasCls(self._core, self._cmd_group)
		return self._sbas

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SelCriteria:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:SELection:MODE \n
		Snippet: value: enums.SelCriteria = driver.source.bb.gnss.sv.selection.get_mode() \n
		Selects a criterium to define the initial satellite constellation. \n
			:return: selection_mode: MANual| ELEVation| VISibility| DOP| ADOP MANual Manual selection to add active space vehicles of the satellite constellation and remove inactive space vehicles from the satellite constellation. You can also activate invisible space vehicles. ELEVation Automatic selection of space vehicles according to their highest elevation angle. VISibility Automatic selection of space vehicles according to their longest visibility time. DOP Automatic selection with good dilution of precision (DOP) values at simulation start. ADOP Adaptive DOP mode providing automatic selection with good DOP values at simulation start and during runtime.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:SELection:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SelCriteria)

	def set_mode(self, selection_mode: enums.SelCriteria) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:SELection:MODE \n
		Snippet: driver.source.bb.gnss.sv.selection.set_mode(selection_mode = enums.SelCriteria.ADOP) \n
		Selects a criterium to define the initial satellite constellation. \n
			:param selection_mode: MANual| ELEVation| VISibility| DOP| ADOP MANual Manual selection to add active space vehicles of the satellite constellation and remove inactive space vehicles from the satellite constellation. You can also activate invisible space vehicles. ELEVation Automatic selection of space vehicles according to their highest elevation angle. VISibility Automatic selection of space vehicles according to their longest visibility time. DOP Automatic selection with good dilution of precision (DOP) values at simulation start. ADOP Adaptive DOP mode providing automatic selection with good DOP values at simulation start and during runtime.
		"""
		param = Conversions.enum_scalar_to_str(selection_mode, enums.SelCriteria)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:MODE {param}')

	def clone(self) -> 'SelectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SelectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
