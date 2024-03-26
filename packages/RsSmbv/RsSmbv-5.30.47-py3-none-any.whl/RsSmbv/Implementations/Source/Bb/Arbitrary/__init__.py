from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ArbitraryCls:
	"""Arbitrary commands group definition. 147 total commands, 10 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("arbitrary", core, parent)

	@property
	def cfr(self):
		"""cfr commands group. 3 Sub-classes, 14 commands."""
		if not hasattr(self, '_cfr'):
			from .Cfr import CfrCls
			self._cfr = CfrCls(self._core, self._cmd_group)
		return self._cfr

	@property
	def clock(self):
		"""clock commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def mcarrier(self):
		"""mcarrier commands group. 9 Sub-classes, 4 commands."""
		if not hasattr(self, '_mcarrier'):
			from .Mcarrier import McarrierCls
			self._mcarrier = McarrierCls(self._core, self._cmd_group)
		return self._mcarrier

	@property
	def notch(self):
		"""notch commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_notch'):
			from .Notch import NotchCls
			self._notch = NotchCls(self._core, self._cmd_group)
		return self._notch

	@property
	def pramp(self):
		"""pramp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pramp'):
			from .Pramp import PrampCls
			self._pramp = PrampCls(self._core, self._cmd_group)
		return self._pramp

	@property
	def signal(self):
		"""signal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_signal'):
			from .Signal import SignalCls
			self._signal = SignalCls(self._core, self._cmd_group)
		return self._signal

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 7 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def tsignal(self):
		"""tsignal commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsignal'):
			from .Tsignal import TsignalCls
			self._tsignal = TsignalCls(self._core, self._cmd_group)
		return self._tsignal

	@property
	def waveform(self):
		"""waveform commands group. 2 Sub-classes, 5 commands."""
		if not hasattr(self, '_waveform'):
			from .Waveform import WaveformCls
			self._waveform = WaveformCls(self._core, self._cmd_group)
		return self._waveform

	@property
	def wsegment(self):
		"""wsegment commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_wsegment'):
			from .Wsegment import WsegmentCls
			self._wsegment = WsegmentCls(self._core, self._cmd_group)
		return self._wsegment

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:PRESet \n
		Snippet: driver.source.bb.arbitrary.preset() \n
		Sets all ARB generator parameters to their default values. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:PRESet \n
		Snippet: driver.source.bb.arbitrary.preset_with_opc() \n
		Sets all ARB generator parameters to their default values. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:STATe \n
		Snippet: value: bool = driver.source.bb.arbitrary.get_state() \n
		Enables the ARB generator. A waveform must be selected before the ARB generator is activated. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:STATe \n
		Snippet: driver.source.bb.arbitrary.set_state(state = False) \n
		Enables the ARB generator. A waveform must be selected before the ARB generator is activated. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:STATe {param}')

	def clone(self) -> 'ArbitraryCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ArbitraryCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
