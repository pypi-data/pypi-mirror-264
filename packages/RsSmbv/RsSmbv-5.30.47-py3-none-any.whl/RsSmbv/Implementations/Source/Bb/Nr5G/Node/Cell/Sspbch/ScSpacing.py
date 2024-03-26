from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScSpacingCls:
	"""ScSpacing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scSpacing", core, parent)

	def set(self, sc_spacing: enums.Numerology, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:SCSPacing \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.scSpacing.set(sc_spacing = enums.Numerology.N120, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects a combination of the subcarrier spacing (SCS) and the cyclic prefix (CP) , where the available values depend on
		the 'Deployment'. See Table 'Supported combinations of SCS and CP per frequency range'. \n
			:param sc_spacing: N15| N30| N60| X60| N120| N240| N480| N960 For the sidelink application, the maximum subcarrier spacing is 120 kHz.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(sc_spacing, enums.Numerology)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:SCSPacing {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> enums.Numerology:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:SCSPacing \n
		Snippet: value: enums.Numerology = driver.source.bb.nr5G.node.cell.sspbch.scSpacing.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects a combination of the subcarrier spacing (SCS) and the cyclic prefix (CP) , where the available values depend on
		the 'Deployment'. See Table 'Supported combinations of SCS and CP per frequency range'. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: sc_spacing: N15| N30| N60| X60| N120| N240| N480| N960 For the sidelink application, the maximum subcarrier spacing is 120 kHz."""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.Numerology)
