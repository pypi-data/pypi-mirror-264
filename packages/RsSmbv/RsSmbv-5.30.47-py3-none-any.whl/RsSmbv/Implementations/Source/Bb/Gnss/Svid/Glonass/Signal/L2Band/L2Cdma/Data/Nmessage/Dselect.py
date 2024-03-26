from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............Internal.Utilities import trim_str_response
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DselectCls:
	"""Dselect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dselect", core, parent)

	def set(self, dselect: str, satelliteSvid=repcap.SatelliteSvid.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIGNal:L2Band:L2CDma<US0>:DATA:NMESsage:DSELect \n
		Snippet: driver.source.bb.gnss.svid.glonass.signal.l2Band.l2Cdma.data.nmessage.dselect.set(dselect = 'abc', satelliteSvid = repcap.SatelliteSvid.Default, indexNull = repcap.IndexNull.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param dselect: string Filename incl. file extension or complete file path
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'L2Cdma')
		"""
		param = Conversions.value_to_quoted_str(dselect)
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIGNal:L2Band:L2CDma{indexNull_cmd_val}:DATA:NMESsage:DSELect {param}')

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default, indexNull=repcap.IndexNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIGNal:L2Band:L2CDma<US0>:DATA:NMESsage:DSELect \n
		Snippet: value: str = driver.source.bb.gnss.svid.glonass.signal.l2Band.l2Cdma.data.nmessage.dselect.get(satelliteSvid = repcap.SatelliteSvid.Default, indexNull = repcap.IndexNull.Default) \n
		Selects an existing data list file from the default directory or from the specific directory. Refer to 'Accessing Files
		in the Default or Specified Directory' for general information on file handling in the default and in a specific
		directory. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'L2Cdma')
			:return: dselect: string Filename incl. file extension or complete file path"""
		satelliteSvid_cmd_val = self._cmd_group.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIGNal:L2Band:L2CDma{indexNull_cmd_val}:DATA:NMESsage:DSELect?')
		return trim_str_response(response)
