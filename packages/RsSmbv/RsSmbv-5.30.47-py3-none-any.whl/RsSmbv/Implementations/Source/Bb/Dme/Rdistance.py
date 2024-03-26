from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RdistanceCls:
	"""Rdistance commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rdistance", core, parent)

	# noinspection PyTypeChecker
	def get_unit(self) -> enums.UnitNmAvionic:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RDIStance:UNIT \n
		Snippet: value: enums.UnitNmAvionic = driver.source.bb.dme.rdistance.get_unit() \n
		Sets the unit for the range distance that can be defined with the [:SOURce<hw>][:BB]:DME:RDIStance. The distance can be
		given in nautic miles (NM) or us. 1 nm is 1852.01 meters and corresponds to a run time of 12.359 us. \n
			:return: unit: US| NM
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RDIStance:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitNmAvionic)

	def set_unit(self, unit: enums.UnitNmAvionic) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RDIStance:UNIT \n
		Snippet: driver.source.bb.dme.rdistance.set_unit(unit = enums.UnitNmAvionic.NM) \n
		Sets the unit for the range distance that can be defined with the [:SOURce<hw>][:BB]:DME:RDIStance. The distance can be
		given in nautic miles (NM) or us. 1 nm is 1852.01 meters and corresponds to a run time of 12.359 us. \n
			:param unit: US| NM
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.UnitNmAvionic)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RDIStance:UNIT {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RDIStance \n
		Snippet: value: float = driver.source.bb.dme.rdistance.get_value() \n
		Sets the simulated distance between the interrogator and the transponder for reply mode (BB:DME:MODE:REPLy) .
		The distance can be given in nautic miles (NM) or us with the command [:SOURce<hw>][:BB]:DME:RDIStance:UNIT. If the unit
		is not provided next to the value, the value is considered to be in the current unit (last unit set via GUI or the SCPI) .
		The query always provides the value in the unit set with [:SOURce<hw>][:BB]:DME:RDIStance:UNIT. The range distance and
		the external trigger delay are interdependent according to: Range distance = (trigger delay - X/Y mode delay) /12.
		359 us/nm (X mode delay = 50 us, Y mode delay is 56 us) Changing one value automatically changes the other value. \n
			:return: rdistance: float Range: -4.046 (X) , -4.531 (Y) to 400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RDIStance?')
		return Conversions.str_to_float(response)

	def set_value(self, rdistance: float) -> None:
		"""SCPI: [SOURce<HW>]:[BB]:DME:RDIStance \n
		Snippet: driver.source.bb.dme.rdistance.set_value(rdistance = 1.0) \n
		Sets the simulated distance between the interrogator and the transponder for reply mode (BB:DME:MODE:REPLy) .
		The distance can be given in nautic miles (NM) or us with the command [:SOURce<hw>][:BB]:DME:RDIStance:UNIT. If the unit
		is not provided next to the value, the value is considered to be in the current unit (last unit set via GUI or the SCPI) .
		The query always provides the value in the unit set with [:SOURce<hw>][:BB]:DME:RDIStance:UNIT. The range distance and
		the external trigger delay are interdependent according to: Range distance = (trigger delay - X/Y mode delay) /12.
		359 us/nm (X mode delay = 50 us, Y mode delay is 56 us) Changing one value automatically changes the other value. \n
			:param rdistance: float Range: -4.046 (X) , -4.531 (Y) to 400
		"""
		param = Conversions.decimal_value_to_str(rdistance)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RDIStance {param}')
