from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImagCls:
	"""Imag commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("imag", core, parent)

	def set(self, cust_const_imag: float, allocationNull=repcap.AllocationNull.Default, constelationPointNull=repcap.ConstelationPointNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:CONPoint<ST0>:IMAG \n
		Snippet: driver.source.bb.ofdm.alloc.conPoint.imag.set(cust_const_imag = 1.0, allocationNull = repcap.AllocationNull.Default, constelationPointNull = repcap.ConstelationPointNull.Default) \n
		Sets the imaginary part of the constellation point of the selected allocation. The imaginary part equals the y-axis value
		in a cartesian coordinate system. \n
			:param cust_const_imag: float Range: -100 to 100
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param constelationPointNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ConPoint')
		"""
		param = Conversions.decimal_value_to_str(cust_const_imag)
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		constelationPointNull_cmd_val = self._cmd_group.get_repcap_cmd_value(constelationPointNull, repcap.ConstelationPointNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:CONPoint{constelationPointNull_cmd_val}:IMAG {param}')

	def get(self, allocationNull=repcap.AllocationNull.Default, constelationPointNull=repcap.ConstelationPointNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:OFDM:ALLoc<CH0>:CONPoint<ST0>:IMAG \n
		Snippet: value: float = driver.source.bb.ofdm.alloc.conPoint.imag.get(allocationNull = repcap.AllocationNull.Default, constelationPointNull = repcap.ConstelationPointNull.Default) \n
		Sets the imaginary part of the constellation point of the selected allocation. The imaginary part equals the y-axis value
		in a cartesian coordinate system. \n
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param constelationPointNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'ConPoint')
			:return: cust_const_imag: float Range: -100 to 100"""
		allocationNull_cmd_val = self._cmd_group.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		constelationPointNull_cmd_val = self._cmd_group.get_repcap_cmd_value(constelationPointNull, repcap.ConstelationPointNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{allocationNull_cmd_val}:CONPoint{constelationPointNull_cmd_val}:IMAG?')
		return Conversions.str_to_float(response)
