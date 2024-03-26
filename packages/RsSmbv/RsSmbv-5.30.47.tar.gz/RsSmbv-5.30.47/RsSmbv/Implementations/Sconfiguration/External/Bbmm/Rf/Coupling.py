from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CouplingCls:
	"""Coupling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coupling", core, parent)

	def set(self, rf_coupling_state: bool, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:RF:COUPling \n
		Snippet: driver.sconfiguration.external.bbmm.rf.coupling.set(rf_coupling_state = False, iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param rf_coupling_state: No help available
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
		"""
		param = Conversions.bool_to_str(rf_coupling_state)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:RF:COUPling {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:BBMM<CH>:RF:COUPling \n
		Snippet: value: bool = driver.sconfiguration.external.bbmm.rf.coupling.get(iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
			:return: rf_coupling_state: No help available"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:BBMM{iqConnector_cmd_val}:RF:COUPling?')
		return Conversions.str_to_bool(response)
