from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbCls:
	"""Bb commands group definition. 8360 total commands, 31 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bb", core, parent)

	@property
	def arbitrary(self):
		"""arbitrary commands group. 10 Sub-classes, 2 commands."""
		if not hasattr(self, '_arbitrary'):
			from .Arbitrary import ArbitraryCls
			self._arbitrary = ArbitraryCls(self._core, self._cmd_group)
		return self._arbitrary

	@property
	def btooth(self):
		"""btooth commands group. 21 Sub-classes, 18 commands."""
		if not hasattr(self, '_btooth'):
			from .Btooth import BtoothCls
			self._btooth = BtoothCls(self._core, self._cmd_group)
		return self._btooth

	@property
	def c2K(self):
		"""c2K commands group. 13 Sub-classes, 5 commands."""
		if not hasattr(self, '_c2K'):
			from .C2K import C2KCls
			self._c2K = C2KCls(self._core, self._cmd_group)
		return self._c2K

	@property
	def coder(self):
		"""coder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coder'):
			from .Coder import CoderCls
			self._coder = CoderCls(self._core, self._cmd_group)
		return self._coder

	@property
	def dab(self):
		"""dab commands group. 11 Sub-classes, 7 commands."""
		if not hasattr(self, '_dab'):
			from .Dab import DabCls
			self._dab = DabCls(self._core, self._cmd_group)
		return self._dab

	@property
	def dme(self):
		"""dme commands group. 14 Sub-classes, 14 commands."""
		if not hasattr(self, '_dme'):
			from .Dme import DmeCls
			self._dme = DmeCls(self._core, self._cmd_group)
		return self._dme

	@property
	def eutra(self):
		"""eutra commands group. 19 Sub-classes, 8 commands."""
		if not hasattr(self, '_eutra'):
			from .Eutra import EutraCls
			self._eutra = EutraCls(self._core, self._cmd_group)
		return self._eutra

	@property
	def evdo(self):
		"""evdo commands group. 13 Sub-classes, 8 commands."""
		if not hasattr(self, '_evdo'):
			from .Evdo import EvdoCls
			self._evdo = EvdoCls(self._core, self._cmd_group)
		return self._evdo

	@property
	def gbas(self):
		"""gbas commands group. 8 Sub-classes, 9 commands."""
		if not hasattr(self, '_gbas'):
			from .Gbas import GbasCls
			self._gbas = GbasCls(self._core, self._cmd_group)
		return self._gbas

	@property
	def gnpr(self):
		"""gnpr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gnpr'):
			from .Gnpr import GnprCls
			self._gnpr = GnprCls(self._core, self._cmd_group)
		return self._gnpr

	@property
	def gnss(self):
		"""gnss commands group. 27 Sub-classes, 6 commands."""
		if not hasattr(self, '_gnss'):
			from .Gnss import GnssCls
			self._gnss = GnssCls(self._core, self._cmd_group)
		return self._gnss

	@property
	def graphics(self):
		"""graphics commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_graphics'):
			from .Graphics import GraphicsCls
			self._graphics = GraphicsCls(self._core, self._cmd_group)
		return self._graphics

	@property
	def gsm(self):
		"""gsm commands group. 17 Sub-classes, 7 commands."""
		if not hasattr(self, '_gsm'):
			from .Gsm import GsmCls
			self._gsm = GsmCls(self._core, self._cmd_group)
		return self._gsm

	@property
	def huwb(self):
		"""huwb commands group. 13 Sub-classes, 12 commands."""
		if not hasattr(self, '_huwb'):
			from .Huwb import HuwbCls
			self._huwb = HuwbCls(self._core, self._cmd_group)
		return self._huwb

	@property
	def impairment(self):
		"""impairment commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_impairment'):
			from .Impairment import ImpairmentCls
			self._impairment = ImpairmentCls(self._core, self._cmd_group)
		return self._impairment

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def lora(self):
		"""lora commands group. 7 Sub-classes, 6 commands."""
		if not hasattr(self, '_lora'):
			from .Lora import LoraCls
			self._lora = LoraCls(self._core, self._cmd_group)
		return self._lora

	@property
	def mccw(self):
		"""mccw commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_mccw'):
			from .Mccw import MccwCls
			self._mccw = MccwCls(self._core, self._cmd_group)
		return self._mccw

	@property
	def nfc(self):
		"""nfc commands group. 10 Sub-classes, 12 commands."""
		if not hasattr(self, '_nfc'):
			from .Nfc import NfcCls
			self._nfc = NfcCls(self._core, self._cmd_group)
		return self._nfc

	@property
	def nr5G(self):
		"""nr5G commands group. 27 Sub-classes, 7 commands."""
		if not hasattr(self, '_nr5G'):
			from .Nr5G import Nr5GCls
			self._nr5G = Nr5GCls(self._core, self._cmd_group)
		return self._nr5G

	@property
	def ofdm(self):
		"""ofdm commands group. 16 Sub-classes, 21 commands."""
		if not hasattr(self, '_ofdm'):
			from .Ofdm import OfdmCls
			self._ofdm = OfdmCls(self._core, self._cmd_group)
		return self._ofdm

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def pramp(self):
		"""pramp commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_pramp'):
			from .Pramp import PrampCls
			self._pramp = PrampCls(self._core, self._cmd_group)
		return self._pramp

	@property
	def progress(self):
		"""progress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_progress'):
			from .Progress import ProgressCls
			self._progress = ProgressCls(self._core, self._cmd_group)
		return self._progress

	@property
	def tdscdma(self):
		"""tdscdma commands group. 12 Sub-classes, 6 commands."""
		if not hasattr(self, '_tdscdma'):
			from .Tdscdma import TdscdmaCls
			self._tdscdma = TdscdmaCls(self._core, self._cmd_group)
		return self._tdscdma

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def vor(self):
		"""vor commands group. 10 Sub-classes, 3 commands."""
		if not hasattr(self, '_vor'):
			from .Vor import VorCls
			self._vor = VorCls(self._core, self._cmd_group)
		return self._vor

	@property
	def w3Gpp(self):
		"""w3Gpp commands group. 13 Sub-classes, 5 commands."""
		if not hasattr(self, '_w3Gpp'):
			from .W3Gpp import W3GppCls
			self._w3Gpp = W3GppCls(self._core, self._cmd_group)
		return self._w3Gpp

	@property
	def wlnn(self):
		"""wlnn commands group. 9 Sub-classes, 8 commands."""
		if not hasattr(self, '_wlnn'):
			from .Wlnn import WlnnCls
			self._wlnn = WlnnCls(self._core, self._cmd_group)
		return self._wlnn

	@property
	def ils(self):
		"""ils commands group. 7 Sub-classes, 3 commands."""
		if not hasattr(self, '_ils'):
			from .Ils import IlsCls
			self._ils = IlsCls(self._core, self._cmd_group)
		return self._ils

	def get_cfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:CFACtor \n
		Snippet: value: float = driver.source.bb.get_cfactor() \n
		Queries the crest factor of the baseband signal. \n
			:return: cfactor: float Range: 0 to 100, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:CFACtor?')
		return Conversions.str_to_float(response)

	def get_foffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: value: float = driver.source.bb.get_foffset() \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:return: foffset: float Range: depends on the installed options , Unit: Hz E.g. -60 MHz to +60 MHz (base unit)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, foffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: driver.source.bb.set_foffset(foffset = 1.0) \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:param foffset: float Range: depends on the installed options , Unit: Hz E.g. -60 MHz to +60 MHz (base unit)
		"""
		param = Conversions.decimal_value_to_str(foffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:FOFFset {param}')

	# noinspection PyTypeChecker
	def get_iq_gain(self) -> enums.IqGain:
		"""SCPI: [SOURce<HW>]:BB:IQGain \n
		Snippet: value: enums.IqGain = driver.source.bb.get_iq_gain() \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:return: ipartq_gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IQGain?')
		return Conversions.str_to_scalar_enum(response, enums.IqGain)

	def set_iq_gain(self, ipartq_gain: enums.IqGain) -> None:
		"""SCPI: [SOURce<HW>]:BB:IQGain \n
		Snippet: driver.source.bb.set_iq_gain(ipartq_gain = enums.IqGain.DB0) \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:param ipartq_gain: DBM4| DBM2| DB0| DB2| DB4| DB8| DB6 Dynamic range of 16 dB divided into 2 dB steps. DB0|DB2|DB4|DB6|DB8 Activates the specified gain of 0 dB, +2 dB, +4 dB, +6 dB, +8 dB DBM2|DBM4 Activates the specified gain of -2 dB, -4 dB
		"""
		param = Conversions.enum_scalar_to_str(ipartq_gain, enums.IqGain)
		self._core.io.write(f'SOURce<HwInstance>:BB:IQGain {param}')

	def get_pgain(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PGAin \n
		Snippet: value: float = driver.source.bb.get_pgain() \n
		No command help available \n
			:return: pgain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PGAin?')
		return Conversions.str_to_float(response)

	def set_pgain(self, pgain: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PGAin \n
		Snippet: driver.source.bb.set_pgain(pgain = 1.0) \n
		No command help available \n
			:param pgain: No help available
		"""
		param = Conversions.decimal_value_to_str(pgain)
		self._core.io.write(f'SOURce<HwInstance>:BB:PGAin {param}')

	def get_poffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: value: float = driver.source.bb.get_poffset() \n
		Sets the relative phase offset for the selected baseband signal. \n
			:return: poffset: float Range: 0 to 359.9, Unit: DEG
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, poffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: driver.source.bb.set_poffset(poffset = 1.0) \n
		Sets the relative phase offset for the selected baseband signal. \n
			:param poffset: float Range: 0 to 359.9, Unit: DEG
		"""
		param = Conversions.decimal_value_to_str(poffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:POFFset {param}')

	# noinspection PyTypeChecker
	def get_route(self) -> enums.PathUniCodBbin:
		"""SCPI: [SOURce<HW>]:BB:ROUTe \n
		Snippet: value: enums.PathUniCodBbin = driver.source.bb.get_route() \n
		Selects the signal route for the internal/external baseband signal. \n
			:return: route: A
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ROUTe?')
		return Conversions.str_to_scalar_enum(response, enums.PathUniCodBbin)

	def set_route(self, route: enums.PathUniCodBbin) -> None:
		"""SCPI: [SOURce<HW>]:BB:ROUTe \n
		Snippet: driver.source.bb.set_route(route = enums.PathUniCodBbin.A) \n
		Selects the signal route for the internal/external baseband signal. \n
			:param route: A
		"""
		param = Conversions.enum_scalar_to_str(route, enums.PathUniCodBbin)
		self._core.io.write(f'SOURce<HwInstance>:BB:ROUTe {param}')

	def clone(self) -> 'BbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
