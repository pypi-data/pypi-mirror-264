from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OsnmaCls:
	"""Osnma commands group definition. 20 total commands, 4 Subgroups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("osnma", core, parent)

	@property
	def aesKey(self):
		"""aesKey commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aesKey'):
			from .AesKey import AesKeyCls
			self._aesKey = AesKeyCls(self._core, self._cmd_group)
		return self._aesKey

	@property
	def ckey(self):
		"""ckey commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ckey'):
			from .Ckey import CkeyCls
			self._ckey = CkeyCls(self._core, self._cmd_group)
		return self._ckey

	@property
	def pkey(self):
		"""pkey commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pkey'):
			from .Pkey import PkeyCls
			self._pkey = PkeyCls(self._core, self._cmd_group)
		return self._pkey

	@property
	def rkey(self):
		"""rkey commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rkey'):
			from .Rkey import RkeyCls
			self._rkey = RkeyCls(self._core, self._cmd_group)
		return self._rkey

	def get_ad_delay(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADDelay \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.get_ad_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADDelay?')
		return Conversions.str_to_int(response)

	def set_ad_delay(self, delay: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADDelay \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_ad_delay(delay = 1) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADDelay {param}')

	def get_adkd(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADKD \n
		Snippet: value: bool = driver.source.bb.gnss.galileo.osnma.get_adkd() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADKD?')
		return Conversions.str_to_bool(response)

	def set_adkd(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:ADKD \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_adkd(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:ADKD {param}')

	# noinspection PyTypeChecker
	def get_hf(self) -> enums.OsnmaHf:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:HF \n
		Snippet: value: enums.OsnmaHf = driver.source.bb.gnss.galileo.osnma.get_hf() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:HF?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaHf)

	def set_hf(self, value: enums.OsnmaHf) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:HF \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_hf(value = enums.OsnmaHf._0) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaHf)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:HF {param}')

	# noinspection PyTypeChecker
	def get_ks(self) -> enums.OsnmaKs:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:KS \n
		Snippet: value: enums.OsnmaKs = driver.source.bb.gnss.galileo.osnma.get_ks() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:KS?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaKs)

	def set_ks(self, value: enums.OsnmaKs) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:KS \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_ks(value = enums.OsnmaKs._0) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaKs)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:KS {param}')

	# noinspection PyTypeChecker
	def get_mac_lt(self) -> enums.OsnmaMaclt:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MACLt \n
		Snippet: value: enums.OsnmaMaclt = driver.source.bb.gnss.galileo.osnma.get_mac_lt() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MACLt?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaMaclt)

	def set_mac_lt(self, value: enums.OsnmaMaclt) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MACLt \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_mac_lt(value = enums.OsnmaMaclt._27) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaMaclt)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MACLt {param}')

	def get_mf(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MF \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.get_mf() \n
		No command help available \n
			:return: mf: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MF?')
		return Conversions.str_to_int(response)

	def set_mf(self, mf: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:MF \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_mf(mf = 1) \n
		No command help available \n
			:param mf: No help available
		"""
		param = Conversions.decimal_value_to_str(mf)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:MF {param}')

	# noinspection PyTypeChecker
	def get_npkt(self) -> enums.OsnmaNpkt:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:NPKT \n
		Snippet: value: enums.OsnmaNpkt = driver.source.bb.gnss.galileo.osnma.get_npkt() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:NPKT?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaNpkt)

	def set_npkt(self, value: enums.OsnmaNpkt) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:NPKT \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_npkt(value = enums.OsnmaNpkt._1) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaNpkt)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:NPKT {param}')

	def get_pid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PID \n
		Snippet: value: int = driver.source.bb.gnss.galileo.osnma.get_pid() \n
		No command help available \n
			:return: pid_input_2: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PID?')
		return Conversions.str_to_int(response)

	def set_pid(self, pid_input_2: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:PID \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_pid(pid_input_2 = 1) \n
		No command help available \n
			:param pid_input_2: No help available
		"""
		param = Conversions.decimal_value_to_str(pid_input_2)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:PID {param}')

	def get_spreemption(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:SPReemption \n
		Snippet: value: bool = driver.source.bb.gnss.galileo.osnma.get_spreemption() \n
		No command help available \n
			:return: status: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:SPReemption?')
		return Conversions.str_to_bool(response)

	def set_spreemption(self, status: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:SPReemption \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_spreemption(status = False) \n
		No command help available \n
			:param status: No help available
		"""
		param = Conversions.bool_to_str(status)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:SPReemption {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.OsnmaTran:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TMODe \n
		Snippet: value: enums.OsnmaTran = driver.source.bb.gnss.galileo.osnma.get_tmode() \n
		No command help available \n
			:return: transition_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaTran)

	def set_tmode(self, transition_mode: enums.OsnmaTran) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TMODe \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_tmode(transition_mode = enums.OsnmaTran.ALERt) \n
		No command help available \n
			:param transition_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(transition_mode, enums.OsnmaTran)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TMODe {param}')

	# noinspection PyTypeChecker
	def get_ts(self) -> enums.OsnmaTs:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TS \n
		Snippet: value: enums.OsnmaTs = driver.source.bb.gnss.galileo.osnma.get_ts() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TS?')
		return Conversions.str_to_scalar_enum(response, enums.OsnmaTs)

	def set_ts(self, value: enums.OsnmaTs) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:GALileo:OSNMa:TS \n
		Snippet: driver.source.bb.gnss.galileo.osnma.set_ts(value = enums.OsnmaTs._5) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_scalar_to_str(value, enums.OsnmaTs)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:GALileo:OSNMa:TS {param}')

	def clone(self) -> 'OsnmaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OsnmaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
