from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HtControlCls:
	"""HtControl commands group definition. 13 total commands, 11 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("htControl", core, parent)

	@property
	def acConstraint(self):
		"""acConstraint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acConstraint'):
			from .AcConstraint import AcConstraintCls
			self._acConstraint = AcConstraintCls(self._core, self._cmd_group)
		return self._acConstraint

	@property
	def calibration(self):
		"""calibration commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def csiSteering(self):
		"""csiSteering commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiSteering'):
			from .CsiSteering import CsiSteeringCls
			self._csiSteering = CsiSteeringCls(self._core, self._cmd_group)
		return self._csiSteering

	@property
	def frequest(self):
		"""frequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequest'):
			from .Frequest import FrequestCls
			self._frequest = FrequestCls(self._core, self._cmd_group)
		return self._frequest

	@property
	def hvIndicator(self):
		"""hvIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hvIndicator'):
			from .HvIndicator import HvIndicatorCls
			self._hvIndicator = HvIndicatorCls(self._core, self._cmd_group)
		return self._hvIndicator

	@property
	def laControl(self):
		"""laControl commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_laControl'):
			from .LaControl import LaControlCls
			self._laControl = LaControlCls(self._core, self._cmd_group)
		return self._laControl

	@property
	def ndp(self):
		"""ndp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndp'):
			from .Ndp import NdpCls
			self._ndp = NdpCls(self._core, self._cmd_group)
		return self._ndp

	@property
	def rdgMore(self):
		"""rdgMore commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdgMore'):
			from .RdgMore import RdgMoreCls
			self._rdgMore = RdgMoreCls(self._core, self._cmd_group)
		return self._rdgMore

	@property
	def reserved(self):
		"""reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reserved'):
			from .Reserved import ReservedCls
			self._reserved = ReservedCls(self._core, self._cmd_group)
		return self._reserved

	@property
	def sreserved(self):
		"""sreserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sreserved'):
			from .Sreserved import SreservedCls
			self._sreserved = SreservedCls(self._core, self._cmd_group)
		return self._sreserved

	@property
	def zlf(self):
		"""zlf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zlf'):
			from .Zlf import ZlfCls
			self._zlf = ZlfCls(self._core, self._cmd_group)
		return self._zlf

	def set(self, ht_control: List[str], frameBlock=repcap.FrameBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl \n
		Snippet: driver.source.bb.wlnn.fblock.mac.htControl.set(ht_control = ['rawAbc1', 'rawAbc2', 'rawAbc3'], frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the HT control field. \n
			:param ht_control: integer Range: #H00000000,32 to #HFFFFFFFF,32
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
		"""
		param = Conversions.list_to_csv_str(ht_control)
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl {param}')

	def get(self, frameBlock=repcap.FrameBlock.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:WLNN:FBLock<CH>:MAC:HTControl \n
		Snippet: value: List[str] = driver.source.bb.wlnn.fblock.mac.htControl.get(frameBlock = repcap.FrameBlock.Default) \n
		Sets the value for the HT control field. \n
			:param frameBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: ht_control: integer Range: #H00000000,32 to #HFFFFFFFF,32"""
		frameBlock_cmd_val = self._cmd_group.get_repcap_cmd_value(frameBlock, repcap.FrameBlock)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{frameBlock_cmd_val}:MAC:HTControl?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'HtControlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HtControlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
