from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RtCls:
	"""Rt commands group definition. 31 total commands, 9 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rt", core, parent)

	@property
	def beidou(self):
		"""beidou commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Beidou import BeidouCls
			self._beidou = BeidouCls(self._core, self._cmd_group)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Galileo import GalileoCls
			self._galileo = GalileoCls(self._core, self._cmd_group)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .Glonass import GlonassCls
			self._glonass = GlonassCls(self._core, self._cmd_group)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Gps import GpsCls
			self._gps = GpsCls(self._core, self._cmd_group)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Navic import NavicCls
			self._navic = NavicCls(self._core, self._cmd_group)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Qzss import QzssCls
			self._qzss = QzssCls(self._core, self._cmd_group)
		return self._qzss

	@property
	def receiver(self):
		"""receiver commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_receiver'):
			from .Receiver import ReceiverCls
			self._receiver = ReceiverCls(self._core, self._cmd_group)
		return self._receiver

	@property
	def sbas(self):
		"""sbas commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .Sbas import SbasCls
			self._sbas = SbasCls(self._core, self._cmd_group)
		return self._sbas

	@property
	def stream(self):
		"""stream commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_stream'):
			from .Stream import StreamCls
			self._stream = StreamCls(self._core, self._cmd_group)
		return self._stream

	def get_hdop(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RT:HDOP \n
		Snippet: value: float = driver.source.bb.gnss.rt.get_hdop() \n
		Queries the horizontal dilution of precision (HDOP) value of the selected satellite constellation. \n
			:return: realtime_hdop: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RT:HDOP?')
		return Conversions.str_to_float(response)

	def get_hw_time(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RT:HWTime \n
		Snippet: value: float = driver.source.bb.gnss.rt.get_hw_time() \n
		Queries the time elapsed since the simulation start. To query the simulation start time, use the command:
		[:SOURce<hw>]:BB:GNSS:TIME:STARt:TIME. \n
			:return: elapsed_time: float Range: 0 to max, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RT:HWTime?')
		return Conversions.str_to_float(response)

	def get_pdop(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RT:PDOP \n
		Snippet: value: float = driver.source.bb.gnss.rt.get_pdop() \n
		Queries the position dilution of precision (PDOP) value of the selected satellite constellation. \n
			:return: realtime_pdop: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RT:PDOP?')
		return Conversions.str_to_float(response)

	def get_vdop(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RT:VDOP \n
		Snippet: value: float = driver.source.bb.gnss.rt.get_vdop() \n
		Queries the vertical dilution of precision (VDOP) value of the selected satellite constellation. \n
			:return: realtime_vdop: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:RT:VDOP?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'RtCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RtCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
