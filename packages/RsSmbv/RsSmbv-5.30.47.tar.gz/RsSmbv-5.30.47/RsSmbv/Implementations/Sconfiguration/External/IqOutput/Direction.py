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
	def get(self, iqConnector=repcap.IqConnector.Default) -> enums.SystConfConnDigStat:
		"""SCPI: SCONfiguration:EXTernal:IQOutput<CH>:DIRection \n
		Snippet: value: enums.SystConfConnDigStat = driver.sconfiguration.external.iqOutput.direction.get(iqConnector = repcap.IqConnector.Default) \n
		Queries the connector direction. \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: direction: NONE| IN| OUT"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:IQOutput{iqConnector_cmd_val}:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfConnDigStat)
