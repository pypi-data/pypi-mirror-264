from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DirectionCls:
	"""Direction commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("direction", core, parent)

	# noinspection PyTypeChecker
	def get(self, index=repcap.Index.Default) -> enums.SystConfConnDigStat:
		"""SCPI: SCONfiguration:EXTernal:HSDigital<CH>:DIRection \n
		Snippet: value: enums.SystConfConnDigStat = driver.sconfiguration.external.hsDigital.direction.get(index = repcap.Index.Default) \n
		Queries the connector direction. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
			:return: direction: NONE| IN| OUT"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:HSDigital{index_cmd_val}:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfConnDigStat)
