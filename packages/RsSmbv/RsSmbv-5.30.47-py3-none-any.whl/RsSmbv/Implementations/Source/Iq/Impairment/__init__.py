from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImpairmentCls:
	"""Impairment commands group definition. 5 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("impairment", core, parent)

	@property
	def iqRatio(self):
		"""iqRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqRatio'):
			from .IqRatio import IqRatioCls
			self._iqRatio = IqRatioCls(self._core, self._cmd_group)
		return self._iqRatio

	@property
	def leakage(self):
		"""leakage commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_leakage'):
			from .Leakage import LeakageCls
			self._leakage = LeakageCls(self._core, self._cmd_group)
		return self._leakage

	@property
	def quadrature(self):
		"""quadrature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_quadrature'):
			from .Quadrature import QuadratureCls
			self._quadrature = QuadratureCls(self._core, self._cmd_group)
		return self._quadrature

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:IMPairment:[STATe] \n
		Snippet: value: bool = driver.source.iq.impairment.get_state() \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:IMPairment:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:IMPairment:[STATe] \n
		Snippet: driver.source.iq.impairment.set_state(state = False) \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:IMPairment:STATe {param}')

	def clone(self) -> 'ImpairmentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ImpairmentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
