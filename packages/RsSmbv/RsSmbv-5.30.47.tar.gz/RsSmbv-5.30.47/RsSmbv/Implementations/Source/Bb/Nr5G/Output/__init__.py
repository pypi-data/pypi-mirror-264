from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 59 total commands, 6 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	@property
	def bbConf(self):
		"""bbConf commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbConf'):
			from .BbConf import BbConfCls
			self._bbConf = BbConfCls(self._core, self._cmd_group)
		return self._bbConf

	@property
	def cfReduction(self):
		"""cfReduction commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_cfReduction'):
			from .CfReduction import CfReductionCls
			self._cfReduction = CfReductionCls(self._core, self._cmd_group)
		return self._cfReduction

	@property
	def filterPy(self):
		"""filterPy commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def power(self):
		"""power commands group. 8 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def ssoc(self):
		"""ssoc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssoc'):
			from .Ssoc import SsocCls
			self._ssoc = SsocCls(self._core, self._cmd_group)
		return self._ssoc

	@property
	def tdWind(self):
		"""tdWind commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdWind'):
			from .TdWind import TdWindCls
			self._tdWind = TdWindCls(self._core, self._cmd_group)
		return self._tdWind

	# noinspection PyTypeChecker
	def get_aclr_opt(self) -> enums.AclrMode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:ACLRopt \n
		Snippet: value: enums.AclrMode = driver.source.bb.nr5G.output.get_aclr_opt() \n
		No command help available \n
			:return: aclr_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:ACLRopt?')
		return Conversions.str_to_scalar_enum(response, enums.AclrMode)

	def set_aclr_opt(self, aclr_mode: enums.AclrMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:ACLRopt \n
		Snippet: driver.source.bb.nr5G.output.set_aclr_opt(aclr_mode = enums.AclrMode.BAL) \n
		No command help available \n
			:param aclr_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(aclr_mode, enums.AclrMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:ACLRopt {param}')

	def get_clevel(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CLEVel \n
		Snippet: value: int = driver.source.bb.nr5G.output.get_clevel() \n
		Sets the limit for level clipping. \n
			:return: clipping_level: integer Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CLEVel?')
		return Conversions.str_to_int(response)

	def set_clevel(self, clipping_level: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CLEVel \n
		Snippet: driver.source.bb.nr5G.output.set_clevel(clipping_level = 1) \n
		Sets the limit for level clipping. \n
			:param clipping_level: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(clipping_level)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CLEVel {param}')

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ClipMode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CMODe \n
		Snippet: value: enums.ClipMode = driver.source.bb.nr5G.output.get_cmode() \n
		Sets the method for level clipping. \n
			:return: clipping_mode: VECTor| SCALar
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ClipMode)

	def set_cmode(self, clipping_mode: enums.ClipMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:CMODe \n
		Snippet: driver.source.bb.nr5G.output.set_cmode(clipping_mode = enums.ClipMode.SCALar) \n
		Sets the method for level clipping. \n
			:param clipping_mode: VECTor| SCALar
		"""
		param = Conversions.enum_scalar_to_str(clipping_mode, enums.ClipMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CMODe {param}')

	# noinspection PyTypeChecker
	def get_fmode(self) -> enums.FilterMode:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:FMODe \n
		Snippet: value: enums.FilterMode = driver.source.bb.nr5G.output.get_fmode() \n
		Defines if and how the filter is applied, on the whole channel bandwidth or on the individual BWPs separately. \n
			:return: filter_bwp: CBW| BWP| OFF| FAST| 2| 1| 0| USER| EVM BWP | 1 Applies a filter to each bandwidth part. CBW | 0 Applies the channel BW filter. EVM Applies a filter to optimze the EVM. FAST | 2 Applies fast filtering. OFF No filter. USER Applies a custom filter.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:FMODe?')
		return Conversions.str_to_scalar_enum(response, enums.FilterMode)

	def set_fmode(self, filter_bwp: enums.FilterMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:FMODe \n
		Snippet: driver.source.bb.nr5G.output.set_fmode(filter_bwp = enums.FilterMode._0) \n
		Defines if and how the filter is applied, on the whole channel bandwidth or on the individual BWPs separately. \n
			:param filter_bwp: CBW| BWP| OFF| FAST| 2| 1| 0| USER| EVM BWP | 1 Applies a filter to each bandwidth part. CBW | 0 Applies the channel BW filter. EVM Applies a filter to optimze the EVM. FAST | 2 Applies fast filtering. OFF No filter. USER Applies a custom filter.
		"""
		param = Conversions.enum_scalar_to_str(filter_bwp, enums.FilterMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:FMODe {param}')

	# noinspection PyTypeChecker
	def get_samr_mode(self) -> enums.SampRateModeRange:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:SAMRmode \n
		Snippet: value: enums.SampRateModeRange = driver.source.bb.nr5G.output.get_samr_mode() \n
		Sets the sample rate mode. \n
			:return: samp_rate_mode: MIN| FFT
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:SAMRmode?')
		return Conversions.str_to_scalar_enum(response, enums.SampRateModeRange)

	def set_samr_mode(self, samp_rate_mode: enums.SampRateModeRange) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:SAMRmode \n
		Snippet: driver.source.bb.nr5G.output.set_samr_mode(samp_rate_mode = enums.SampRateModeRange.FFT) \n
		Sets the sample rate mode. \n
			:param samp_rate_mode: MIN| FFT
		"""
		param = Conversions.enum_scalar_to_str(samp_rate_mode, enums.SampRateModeRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:SAMRmode {param}')

	def get_seq_len(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:SEQLen \n
		Snippet: value: int = driver.source.bb.nr5G.output.get_seq_len() \n
		Sets the sequence length of the signal in number of frames. \n
			:return: seq_len: integer Range: 1 to depends on settings
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:SEQLen?')
		return Conversions.str_to_int(response)

	def set_seq_len(self, seq_len: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:SEQLen \n
		Snippet: driver.source.bb.nr5G.output.set_seq_len(seq_len = 1) \n
		Sets the sequence length of the signal in number of frames. \n
			:param seq_len: integer Range: 1 to depends on settings
		"""
		param = Conversions.decimal_value_to_str(seq_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:SEQLen {param}')

	def get_suslen(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:SUSLen \n
		Snippet: value: int = driver.source.bb.nr5G.output.get_suslen() \n
		Sets the sequence length of the signal in terms of subframes. \n
			:return: seq_len_subfr: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:SUSLen?')
		return Conversions.str_to_int(response)

	def set_suslen(self, seq_len_subfr: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:OUTPut:SUSLen \n
		Snippet: driver.source.bb.nr5G.output.set_suslen(seq_len_subfr = 1) \n
		Sets the sequence length of the signal in terms of subframes. \n
			:param seq_len_subfr: integer Range: 1 to device dependent
		"""
		param = Conversions.decimal_value_to_str(seq_len_subfr)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:SUSLen {param}')

	def clone(self) -> 'OutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
