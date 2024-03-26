from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhymacCfgCls:
	"""PhymacCfg commands group definition. 7 total commands, 1 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phymacCfg", core, parent)

	@property
	def dpattern(self):
		"""dpattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpattern'):
			from .Dpattern import DpatternCls
			self._dpattern = DpatternCls(self._core, self._cmd_group)
		return self._dpattern

	# noinspection PyTypeChecker
	def get_coderate(self) -> enums.BtoCodeRate:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:CODERate \n
		Snippet: value: enums.BtoCodeRate = driver.source.bb.btooth.phymacCfg.get_coderate() \n
		No command help available \n
			:return: coderate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:CODERate?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCodeRate)

	def set_coderate(self, coderate: enums.BtoCodeRate) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:CODERate \n
		Snippet: driver.source.bb.btooth.phymacCfg.set_coderate(coderate = enums.BtoCodeRate.CR_12) \n
		No command help available \n
			:param coderate: No help available
		"""
		param = Conversions.enum_scalar_to_str(coderate, enums.BtoCodeRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:CODERate {param}')

	def get_dselection(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:DSELection \n
		Snippet: value: str = driver.source.bb.btooth.phymacCfg.get_dselection() \n
		No command help available \n
			:return: dselection: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, dselection: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:DSELection \n
		Snippet: driver.source.bb.btooth.phymacCfg.set_dselection(dselection = 'abc') \n
		No command help available \n
			:param dselection: No help available
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:DSELection {param}')

	# noinspection PyTypeChecker
	def get_mac_header(self) -> enums.DataSourceB:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:MACHeader \n
		Snippet: value: enums.DataSourceB = driver.source.bb.btooth.phymacCfg.get_mac_header() \n
		No command help available \n
			:return: mac_header: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:MACHeader?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceB)

	def set_mac_header(self, mac_header: enums.DataSourceB) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:MACHeader \n
		Snippet: driver.source.bb.btooth.phymacCfg.set_mac_header(mac_header = enums.DataSourceB.ALL0) \n
		No command help available \n
			:param mac_header: No help available
		"""
		param = Conversions.enum_scalar_to_str(mac_header, enums.DataSourceB)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:MACHeader {param}')

	# noinspection PyTypeChecker
	def get_payload_cod(self) -> enums.BtoHdrpPayload:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:PAYLoadCod \n
		Snippet: value: enums.BtoHdrpPayload = driver.source.bb.btooth.phymacCfg.get_payload_cod() \n
		No command help available \n
			:return: payload_coding: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:PAYLoadCod?')
		return Conversions.str_to_scalar_enum(response, enums.BtoHdrpPayload)

	def set_payload_cod(self, payload_coding: enums.BtoHdrpPayload) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:PAYLoadCod \n
		Snippet: driver.source.bb.btooth.phymacCfg.set_payload_cod(payload_coding = enums.BtoHdrpPayload.LDPCCOD) \n
		No command help available \n
			:param payload_coding: No help available
		"""
		param = Conversions.enum_scalar_to_str(payload_coding, enums.BtoHdrpPayload)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:PAYLoadCod {param}')

	def get_payload_len(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:PAYLoadLen \n
		Snippet: value: int = driver.source.bb.btooth.phymacCfg.get_payload_len() \n
		No command help available \n
			:return: pay_len: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:PAYLoadLen?')
		return Conversions.str_to_int(response)

	def set_payload_len(self, pay_len: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:PAYLoadLen \n
		Snippet: driver.source.bb.btooth.phymacCfg.set_payload_len(pay_len = 1) \n
		No command help available \n
			:param pay_len: No help available
		"""
		param = Conversions.decimal_value_to_str(pay_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:PAYLoadLen {param}')

	def get_prt_aggre(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:PRTAggre \n
		Snippet: value: bool = driver.source.bb.btooth.phymacCfg.get_prt_aggre() \n
		No command help available \n
			:return: parity_aggregation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:PRTAggre?')
		return Conversions.str_to_bool(response)

	def set_prt_aggre(self, parity_aggregation: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:PHYMacCfg:PRTAggre \n
		Snippet: driver.source.bb.btooth.phymacCfg.set_prt_aggre(parity_aggregation = False) \n
		No command help available \n
			:param parity_aggregation: No help available
		"""
		param = Conversions.bool_to_str(parity_aggregation)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PHYMacCfg:PRTAggre {param}')

	def clone(self) -> 'PhymacCfgCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PhymacCfgCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
