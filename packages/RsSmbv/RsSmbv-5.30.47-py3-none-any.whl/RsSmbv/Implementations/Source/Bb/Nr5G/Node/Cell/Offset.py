from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, offset_relative_t: enums.OffsetRelativeAll, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:OFFSet \n
		Snippet: driver.source.bb.nr5G.node.cell.offset.set(offset_relative_t = enums.OffsetRelativeAll.POINta, cellNull = repcap.CellNull.Default) \n
		Defines the reference point, relative to which the SS/PBCH is allocated in frequency domain.
		For the sidelink application: the reference point of the S-SS/PSBCH is always the reference point A. \n
			:param offset_relative_t: TXBW| POINta TXBW The frequency position of the SS/PBCH is set relative to the usable RBs that apply for the current numerology, i.e. to the start of the TxBWs. POINta The frequency position of the SS/PBCH is set relative to the position of point A.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
		"""
		param = Conversions.enum_scalar_to_str(offset_relative_t, enums.OffsetRelativeAll)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:OFFSet {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default) -> enums.OffsetRelativeAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:OFFSet \n
		Snippet: value: enums.OffsetRelativeAll = driver.source.bb.nr5G.node.cell.offset.get(cellNull = repcap.CellNull.Default) \n
		Defines the reference point, relative to which the SS/PBCH is allocated in frequency domain.
		For the sidelink application: the reference point of the S-SS/PSBCH is always the reference point A. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: offset_relative_t: TXBW| POINta TXBW The frequency position of the SS/PBCH is set relative to the usable RBs that apply for the current numerology, i.e. to the start of the TxBWs. POINta The frequency position of the SS/PBCH is set relative to the position of point A."""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:OFFSet?')
		return Conversions.str_to_scalar_enum(response, enums.OffsetRelativeAll)
