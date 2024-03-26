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

	def set(self, rf_coupling_state: bool, path=repcap.Path.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:COUPling \n
		Snippet: driver.sconfiguration.external.rf.rf.coupling.set(rf_coupling_state = False, path = repcap.Path.Default) \n
		No command help available \n
			:param rf_coupling_state: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = Conversions.bool_to_str(rf_coupling_state)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:COUPling {param}')

	def get(self, path=repcap.Path.Default) -> bool:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:COUPling \n
		Snippet: value: bool = driver.sconfiguration.external.rf.rf.coupling.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: rf_coupling_state: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:COUPling?')
		return Conversions.str_to_bool(response)
