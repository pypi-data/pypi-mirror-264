from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ToaDataCls:
	"""ToaData commands group definition. 7 total commands, 0 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("toaData", core, parent)

	# noinspection PyTypeChecker
	class DateStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Year: int: integer Range: 1980 to 9999
			- Month: int: integer Range: 1 to 12
			- Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def get_date(self) -> DateStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:DATE \n
		Snippet: value: DateStruct = driver.source.bb.gnss.adGeneration.glonass.toaData.get_date() \n
		Enabled for UTC or GLONASS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Enters the date for the
		assistance data in DMS format of the Gregorian calendar. \n
			:return: structure: for return value, see the help for DateStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:DATE?', self.__class__.DateStruct())

	def get_duration(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:DURation \n
		Snippet: value: float = driver.source.bb.gnss.adGeneration.glonass.toaData.get_duration() \n
		Sets the duration of the assistance data. \n
			:return: duration: float Range: 1E-3 to 5E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:DURation?')
		return Conversions.str_to_float(response)

	def set_duration(self, duration: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:DURation \n
		Snippet: driver.source.bb.gnss.adGeneration.glonass.toaData.set_duration(duration = 1.0) \n
		Sets the duration of the assistance data. \n
			:param duration: float Range: 1E-3 to 5E3
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:DURation {param}')

	def get_resolution(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:RESolution \n
		Snippet: value: float = driver.source.bb.gnss.adGeneration.glonass.toaData.get_resolution() \n
		Sets the resolution of the assistance data. \n
			:return: resolution: float Range: 1E-3 to 5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:RESolution?')
		return Conversions.str_to_float(response)

	def set_resolution(self, resolution: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:RESolution \n
		Snippet: driver.source.bb.gnss.adGeneration.glonass.toaData.set_resolution(resolution = 1.0) \n
		Sets the resolution of the assistance data. \n
			:param resolution: float Range: 1E-3 to 5
		"""
		param = Conversions.decimal_value_to_str(resolution)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:RESolution {param}')

	# noinspection PyTypeChecker
	def get_tbasis(self) -> enums.TimeBasis:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:TBASis \n
		Snippet: value: enums.TimeBasis = driver.source.bb.gnss.adGeneration.glonass.toaData.get_tbasis() \n
		Determines the timebase used to enter the time of assistance data parameters. \n
			:return: time_basis: UTC| GPS| GST| GLO| BDT| NAV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:TBASis?')
		return Conversions.str_to_scalar_enum(response, enums.TimeBasis)

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Hour: int: integer Range: 0 to 23
			- Minute: int: integer Range: 0 to 59
			- Second: float: float Range: 0 to 59.999"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_float('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: float = None

	def get_time(self) -> TimeStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:TIME \n
		Snippet: value: TimeStruct = driver.source.bb.gnss.adGeneration.glonass.toaData.get_time() \n
		Enabled for UTC or GLONASS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Enters the exact start time
		for the assistance data in UTC time format. \n
			:return: structure: for return value, see the help for TimeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:TIME?', self.__class__.TimeStruct())

	def get_to_week(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:TOWeek \n
		Snippet: value: int = driver.source.bb.gnss.adGeneration.glonass.toaData.get_to_week() \n
		Enabled for GPS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Determines the Time of Week (TOW) the
		assistance data is generated for. \n
			:return: tow: integer Range: -604800 to 604800
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:TOWeek?')
		return Conversions.str_to_int(response)

	def get_wnumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GLONass:TOAData:WNUMber \n
		Snippet: value: int = driver.source.bb.gnss.adGeneration.glonass.toaData.get_wnumber() \n
		Enabled for GPS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:QZSS:TOAData:TBASis) . Sets the week number (WN) the
		assistance data is generated for. \n
			:return: week_number: integer Range: 0 to 9999.0*53
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GLONass:TOAData:WNUMber?')
		return Conversions.str_to_int(response)
