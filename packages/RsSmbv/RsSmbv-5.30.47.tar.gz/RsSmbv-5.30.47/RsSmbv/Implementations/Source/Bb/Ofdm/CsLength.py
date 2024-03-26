from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsLengthCls:
	"""CsLength commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: CoresetLength, default value after init: CoresetLength.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csLength", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_coresetLength_get', 'repcap_coresetLength_set', repcap.CoresetLength.Nr1)

	def repcap_coresetLength_set(self, coresetLength: repcap.CoresetLength) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CoresetLength.Default
		Default value after init: CoresetLength.Nr1"""
		self._cmd_group.set_repcap_enum_value(coresetLength)

	def repcap_coresetLength_get(self) -> repcap.CoresetLength:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, cyc_suff_len: int, coresetLength=repcap.CoresetLength.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:OFDM:CSLength<CH> \n
		Snippet: driver.source.bb.ofdm.csLength.set(cyc_suff_len = 1, coresetLength = repcap.CoresetLength.Default) \n
		Sets the cyclic suffix length.
		The maximum length equals the total number of sucarriers: [:SOURce<hw>]:BB:OFDM:NSUBcarriers \n
			:param cyc_suff_len: integer Range: 0 to depends on settings
			:param coresetLength: optional repeated capability selector. Default value: Nr1 (settable in the interface 'CsLength')
		"""
		param = Conversions.decimal_value_to_str(cyc_suff_len)
		coresetLength_cmd_val = self._cmd_group.get_repcap_cmd_value(coresetLength, repcap.CoresetLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:CSLength{coresetLength_cmd_val} {param}')

	def get(self, coresetLength=repcap.CoresetLength.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:OFDM:CSLength<CH> \n
		Snippet: value: int = driver.source.bb.ofdm.csLength.get(coresetLength = repcap.CoresetLength.Default) \n
		Sets the cyclic suffix length.
		The maximum length equals the total number of sucarriers: [:SOURce<hw>]:BB:OFDM:NSUBcarriers \n
			:param coresetLength: optional repeated capability selector. Default value: Nr1 (settable in the interface 'CsLength')
			:return: cyc_suff_len: integer Range: 0 to depends on settings"""
		coresetLength_cmd_val = self._cmd_group.get_repcap_cmd_value(coresetLength, repcap.CoresetLength)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:CSLength{coresetLength_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'CsLengthCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsLengthCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
