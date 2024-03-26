from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModulationCls:
	"""Modulation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modulation", core, parent)

	def set(self, modulation: enums.ModType, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:DUMRes:MODulation \n
		Snippet: driver.source.bb.nr5G.node.cell.dumRes.modulation.set(modulation = enums.ModType.BPSK, cellNull = repcap.CellNull.Default) \n
		Sets the modulation scheme for the dummy REs. \n
			:param modulation: BPSK| BPSK2| QPSK| QAM16| QAM64| QAM256| QAM1024
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.enum_scalar_to_str(modulation, enums.ModType)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:DUMRes:MODulation {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.ModType:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:DUMRes:MODulation \n
		Snippet: value: enums.ModType = driver.source.bb.nr5G.node.cell.dumRes.modulation.get(cellNull = repcap.CellNull.Default) \n
		Sets the modulation scheme for the dummy REs. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: modulation: BPSK| BPSK2| QPSK| QAM16| QAM64| QAM256| QAM1024"""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:DUMRes:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModType)
