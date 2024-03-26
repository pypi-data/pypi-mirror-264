from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsCls:
	"""Cs commands group definition. 108 total commands, 9 Subgroups, 13 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cs", core, parent)

	@property
	def cdata(self):
		"""cdata commands group. 4 Sub-classes, 44 commands."""
		if not hasattr(self, '_cdata'):
			from .Cdata import CdataCls
			self._cdata = CdataCls(self._core, self._cmd_group)
		return self._cdata

	@property
	def cinc(self):
		"""cinc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cinc'):
			from .Cinc import CincCls
			self._cinc = CincCls(self._core, self._cmd_group)
		return self._cinc

	@property
	def cinp(self):
		"""cinp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cinp'):
			from .Cinp import CinpCls
			self._cinp = CinpCls(self._core, self._cmd_group)
		return self._cinp

	@property
	def civc(self):
		"""civc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_civc'):
			from .Civc import CivcCls
			self._civc = CivcCls(self._core, self._cmd_group)
		return self._civc

	@property
	def civp(self):
		"""civp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_civp'):
			from .Civp import CivpCls
			self._civp = CivpCls(self._core, self._cmd_group)
		return self._civp

	@property
	def cpvc(self):
		"""cpvc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpvc'):
			from .Cpvc import CpvcCls
			self._cpvc = CpvcCls(self._core, self._cmd_group)
		return self._cpvc

	@property
	def cpvp(self):
		"""cpvp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpvp'):
			from .Cpvp import CpvpCls
			self._cpvp = CpvpCls(self._core, self._cmd_group)
		return self._cpvp

	@property
	def correctionTable(self):
		"""correctionTable commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_correctionTable'):
			from .CorrectionTable import CorrectionTableCls
			self._correctionTable = CorrectionTableCls(self._core, self._cmd_group)
		return self._correctionTable

	@property
	def sevent(self):
		"""sevent commands group. 23 Sub-classes, 0 commands."""
		if not hasattr(self, '_sevent'):
			from .Sevent import SeventCls
			self._sevent = SeventCls(self._core, self._cmd_group)
		return self._sevent

	# noinspection PyTypeChecker
	class CfChmStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Cs_Filtered_Ch_M: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Cs_Filtered_Ch_M', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cs_Filtered_Ch_M: List[str] = None
			self.Bitcount: int = None

	def get_cf_chm(self) -> CfChmStruct:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CFCHm \n
		Snippet: value: CfChmStruct = driver.source.bb.btooth.cs.get_cf_chm() \n
		No command help available \n
			:return: structure: for return value, see the help for CfChmStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:CS:CFCHm?', self.__class__.CfChmStruct())

	def get_cinterval(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINTerval \n
		Snippet: value: float = driver.source.bb.btooth.cs.get_cinterval() \n
		No command help available \n
			:return: connect_interval: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CINTerval?')
		return Conversions.str_to_float(response)

	def set_cinterval(self, connect_interval: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CINTerval \n
		Snippet: driver.source.bb.btooth.cs.set_cinterval(connect_interval = 1.0) \n
		No command help available \n
			:param connect_interval: No help available
		"""
		param = Conversions.decimal_value_to_str(connect_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CINTerval {param}')

	def get_cm_repetition(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CMRepetition \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_cm_repetition() \n
		No command help available \n
			:return: chm_repetition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CMRepetition?')
		return Conversions.str_to_int(response)

	def set_cm_repetition(self, chm_repetition: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CMRepetition \n
		Snippet: driver.source.bb.btooth.cs.set_cm_repetition(chm_repetition = 1) \n
		No command help available \n
			:param chm_repetition: No help available
		"""
		param = Conversions.decimal_value_to_str(chm_repetition)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CMRepetition {param}')

	# noinspection PyTypeChecker
	def get_csel(self) -> enums.BtoCsChSel:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSEL \n
		Snippet: value: enums.BtoCsChSel = driver.source.bb.btooth.cs.get_csel() \n
		No command help available \n
			:return: ch_sel: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CSEL?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsChSel)

	def set_csel(self, ch_sel: enums.BtoCsChSel) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CSEL \n
		Snippet: driver.source.bb.btooth.cs.set_csel(ch_sel = enums.BtoCsChSel.SEL_3B) \n
		No command help available \n
			:param ch_sel: No help available
		"""
		param = Conversions.enum_scalar_to_str(ch_sel, enums.BtoCsChSel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CSEL {param}')

	# noinspection PyTypeChecker
	def get_ctc_jump(self) -> enums.BtoCsCh3Cjump:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCJump \n
		Snippet: value: enums.BtoCsCh3Cjump = driver.source.bb.btooth.cs.get_ctc_jump() \n
		No command help available \n
			:return: ch_three_cjump: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CTCJump?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCh3Cjump)

	def set_ctc_jump(self, ch_three_cjump: enums.BtoCsCh3Cjump) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCJump \n
		Snippet: driver.source.bb.btooth.cs.set_ctc_jump(ch_three_cjump = enums.BtoCsCh3Cjump.JUMP_2) \n
		No command help available \n
			:param ch_three_cjump: No help available
		"""
		param = Conversions.enum_scalar_to_str(ch_three_cjump, enums.BtoCsCh3Cjump)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CTCJump {param}')

	# noinspection PyTypeChecker
	def get_ctc_shape(self) -> enums.BtoCsCh3Cshape:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCShape \n
		Snippet: value: enums.BtoCsCh3Cshape = driver.source.bb.btooth.cs.get_ctc_shape() \n
		No command help available \n
			:return: ch_three_cshape: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:CTCShape?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsCh3Cshape)

	def set_ctc_shape(self, ch_three_cshape: enums.BtoCsCh3Cshape) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:CTCShape \n
		Snippet: driver.source.bb.btooth.cs.set_ctc_shape(ch_three_cshape = enums.BtoCsCh3Cshape.HAT) \n
		No command help available \n
			:param ch_three_cshape: No help available
		"""
		param = Conversions.enum_scalar_to_str(ch_three_cshape, enums.BtoCsCh3Cshape)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:CTCShape {param}')

	def get_einterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_einterval() \n
		No command help available \n
			:return: event_interval: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:EINTerval?')
		return Conversions.str_to_int(response)

	def set_einterval(self, event_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EINTerval \n
		Snippet: driver.source.bb.btooth.cs.set_einterval(event_interval = 1) \n
		No command help available \n
			:param event_interval: No help available
		"""
		param = Conversions.decimal_value_to_str(event_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:EINTerval {param}')

	def get_eoffset(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EOFFset \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_eoffset() \n
		No command help available \n
			:return: event_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:EOFFset?')
		return Conversions.str_to_int(response)

	def set_eoffset(self, event_offset: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:EOFFset \n
		Snippet: driver.source.bb.btooth.cs.set_eoffset(event_offset = 1) \n
		No command help available \n
			:param event_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(event_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:EOFFset {param}')

	# noinspection PyTypeChecker
	def get_role(self) -> enums.BtoCsRoles:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:ROLE \n
		Snippet: value: enums.BtoCsRoles = driver.source.bb.btooth.cs.get_role() \n
		No command help available \n
			:return: role: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:ROLE?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsRoles)

	def set_role(self, role: enums.BtoCsRoles) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:ROLE \n
		Snippet: driver.source.bb.btooth.cs.set_role(role = enums.BtoCsRoles.INITIATOR) \n
		No command help available \n
			:param role: No help available
		"""
		param = Conversions.enum_scalar_to_str(role, enums.BtoCsRoles)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:ROLE {param}')

	def get_sinterval(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SINTerval \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_sinterval() \n
		No command help available \n
			:return: sub_interval: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SINTerval?')
		return Conversions.str_to_int(response)

	def set_sinterval(self, sub_interval: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SINTerval \n
		Snippet: driver.source.bb.btooth.cs.set_sinterval(sub_interval = 1) \n
		No command help available \n
			:param sub_interval: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SINTerval {param}')

	def get_slength(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SLENgth \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_slength() \n
		No command help available \n
			:return: sub_length: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, sub_length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SLENgth \n
		Snippet: driver.source.bb.btooth.cs.set_slength(sub_length = 1) \n
		No command help available \n
			:param sub_length: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SLENgth {param}')

	def get_snumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SNUMber \n
		Snippet: value: int = driver.source.bb.btooth.cs.get_snumber() \n
		No command help available \n
			:return: sub_number: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SNUMber?')
		return Conversions.str_to_int(response)

	def set_snumber(self, sub_number: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SNUMber \n
		Snippet: driver.source.bb.btooth.cs.set_snumber(sub_number = 1) \n
		No command help available \n
			:param sub_number: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SNUMber {param}')

	# noinspection PyTypeChecker
	def get_sscheduling(self) -> enums.AutoManualModeB:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SSCHeduling \n
		Snippet: value: enums.AutoManualModeB = driver.source.bb.btooth.cs.get_sscheduling() \n
		No command help available \n
			:return: step_scheduling: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CS:SSCHeduling?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualModeB)

	def set_sscheduling(self, step_scheduling: enums.AutoManualModeB) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:SSCHeduling \n
		Snippet: driver.source.bb.btooth.cs.set_sscheduling(step_scheduling = enums.AutoManualModeB.AUTO) \n
		No command help available \n
			:param step_scheduling: No help available
		"""
		param = Conversions.enum_scalar_to_str(step_scheduling, enums.AutoManualModeB)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SSCHeduling {param}')

	def clone(self) -> 'CsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
