from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	def get(self, vehicle=repcap.Vehicle.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:CATalog \n
		Snippet: value: List[str] = driver.source.bb.gnss.receiver.v.location.catalog.get(vehicle = repcap.Vehicle.Default) \n
		Queries the names of predefined geographic locations of the GNSS receiver. The query returns a comma-separated list of
		available locations. For predefined geographic locations, see Table 'Coordinates of the simulated predefined positions'. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: gnss_location_names: No help available"""
		vehicle_cmd_val = self._cmd_group.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:LOCation:CATalog?')
		return Conversions.str_to_str_list(response)
