from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, power_offset: float, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:RF:POWer:OFFSet \n
		Snippet: driver.sconfiguration.external.iqOutput.rf.power.offset.set(power_offset = 1.0, iqConnector = repcap.IqConnector.Default) \n
		In coupled mode, offsets the RF level of the external instrument with the selected delta value. \n
			:param power_offset: float Range: -100 to 100
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		param = Conversions.decimal_value_to_str(power_offset)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:RF:POWer:OFFSet {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:RF:POWer:OFFSet \n
		Snippet: value: float = driver.sconfiguration.external.iqOutput.rf.power.offset.get(iqConnector = repcap.IqConnector.Default) \n
		In coupled mode, offsets the RF level of the external instrument with the selected delta value. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: power_offset: float Range: -100 to 100"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:RF:POWer:OFFSet?')
		return Conversions.str_to_float(response)
