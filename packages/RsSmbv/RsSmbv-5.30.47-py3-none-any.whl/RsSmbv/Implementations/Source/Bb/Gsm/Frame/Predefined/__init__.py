from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PredefinedCls:
	"""Predefined commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("predefined", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	def load(self, filename: str, frameIx=repcap.FrameIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GSM:[FRAMe<DI>]:PREDefined:LOAD \n
		Snippet: driver.source.bb.gsm.frame.predefined.load(filename = 'abc', frameIx = repcap.FrameIx.Default) \n
		This command loads the selected file with predefined frame settings. The directory is pre-set, therefore a path cannot be
		specified. \n
			:param filename: string
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
		"""
		param = Conversions.value_to_quoted_str(filename)
		frameIx_cmd_val = self._cmd_group.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:PREDefined:LOAD {param}')

	def clone(self) -> 'PredefinedCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PredefinedCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
