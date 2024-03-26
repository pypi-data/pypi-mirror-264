from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrmFormatCls:
	"""FrmFormat commands group definition. 11 total commands, 2 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frmFormat", core, parent)

	@property
	def iab(self):
		"""iab commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iab'):
			from .Iab import IabCls
			self._iab = IabCls(self._core, self._cmd_group)
		return self._iab

	@property
	def ssc(self):
		"""ssc commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_ssc'):
			from .Ssc import SscCls
			self._ssc = SscCls(self._core, self._cmd_group)
		return self._ssc

	def get_ndl_slots(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NDLSlots \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.get_ndl_slots() \n
		Sets the number of DL slots in the frame. \n
			:return: qck_set_dl_slots: integer Range: 0 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NDLSlots?')
		return Conversions.str_to_int(response)

	def set_ndl_slots(self, qck_set_dl_slots: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NDLSlots \n
		Snippet: driver.source.bb.nr5G.qckset.frmFormat.set_ndl_slots(qck_set_dl_slots = 1) \n
		Sets the number of DL slots in the frame. \n
			:param qck_set_dl_slots: integer Range: 0 to 10
		"""
		param = Conversions.decimal_value_to_str(qck_set_dl_slots)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NDLSlots {param}')

	def get_ns_slots(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NSSLots \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.get_ns_slots() \n
		Queries the number of special slots in the frame. \n
			:return: qck_set_no_spl_slot: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NSSLots?')
		return Conversions.str_to_int(response)

	def get_nul_slots(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NULSlots \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.get_nul_slots() \n
		Queries the number of UL slots in the frame. \n
			:return: qck_set_ul_slots: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NULSlots?')
		return Conversions.str_to_int(response)

	def set_nul_slots(self, qck_set_ul_slots: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NULSlots \n
		Snippet: driver.source.bb.nr5G.qckset.frmFormat.set_nul_slots(qck_set_ul_slots = 1) \n
		Queries the number of UL slots in the frame. \n
			:param qck_set_ul_slots: integer Range: 0 to 10
		"""
		param = Conversions.decimal_value_to_str(qck_set_ul_slots)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NULSlots {param}')

	# noinspection PyTypeChecker
	def get_slength(self) -> enums.QuickSetSlotLenAll:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SLENgth \n
		Snippet: value: enums.QuickSetSlotLenAll = driver.source.bb.nr5G.qckset.frmFormat.get_slength() \n
		No command help available \n
			:return: qck_set_slot_len: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SLENgth?')
		return Conversions.str_to_scalar_enum(response, enums.QuickSetSlotLenAll)

	def set_slength(self, qck_set_slot_len: enums.QuickSetSlotLenAll) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SLENgth \n
		Snippet: driver.source.bb.nr5G.qckset.frmFormat.set_slength(qck_set_slot_len = enums.QuickSetSlotLenAll.S10) \n
		No command help available \n
			:param qck_set_slot_len: No help available
		"""
		param = Conversions.enum_scalar_to_str(qck_set_slot_len, enums.QuickSetSlotLenAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SLENgth {param}')

	def get_slint(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SLINt \n
		Snippet: value: int = driver.source.bb.nr5G.qckset.frmFormat.get_slint() \n
		Sets the duration of the frame in slots. \n
			:return: slot_length_int: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SLINt?')
		return Conversions.str_to_int(response)

	def set_slint(self, slot_length_int: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SLINt \n
		Snippet: driver.source.bb.nr5G.qckset.frmFormat.set_slint(slot_length_int = 1) \n
		Sets the duration of the frame in slots. \n
			:param slot_length_int: integer Range: 2 to 20
		"""
		param = Conversions.decimal_value_to_str(slot_length_int)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SLINt {param}')

	def clone(self) -> 'FrmFormatCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrmFormatCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
