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

	def set(self, rf_coupling_state: bool, index=repcap.Index.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:RF:COUPling \n
		Snippet: driver.sconfiguration.external.digital.rf.coupling.set(rf_coupling_state = False, index = repcap.Index.Default) \n
		Enables/disables coupling all major RF setting (like the frequency, level and RF state) of the external instrument to the
		R&S SMBV100B. \n
			:param rf_coupling_state: 1| ON| 0| OFF
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
		"""
		param = Conversions.bool_to_str(rf_coupling_state)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:RF:COUPling {param}')

	def get(self, index=repcap.Index.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:DIGital<CH>:RF:COUPling \n
		Snippet: value: bool = driver.sconfiguration.external.digital.rf.coupling.get(index = repcap.Index.Default) \n
		Enables/disables coupling all major RF setting (like the frequency, level and RF state) of the external instrument to the
		R&S SMBV100B. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Digital')
			:return: rf_coupling_state: 1| ON| 0| OFF"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:DIGital{index_cmd_val}:RF:COUPling?')
		return Conversions.str_to_bool(response)
