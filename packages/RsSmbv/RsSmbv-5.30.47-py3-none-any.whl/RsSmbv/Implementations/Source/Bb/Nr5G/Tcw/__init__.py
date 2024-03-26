from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TcwCls:
	"""Tcw commands group definition. 82 total commands, 11 Subgroups, 16 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tcw", core, parent)

	@property
	def ant(self):
		"""ant commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ant'):
			from .Ant import AntCls
			self._ant = AntCls(self._core, self._cmd_group)
		return self._ant

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	@property
	def awgn(self):
		"""awgn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_awgn'):
			from .Awgn import AwgnCls
			self._awgn = AwgnCls(self._core, self._cmd_group)
		return self._awgn

	@property
	def fa(self):
		"""fa commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fa'):
			from .Fa import FaCls
			self._fa = FaCls(self._core, self._cmd_group)
		return self._fa

	@property
	def is2(self):
		"""is2 commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_is2'):
			from .Is2 import Is2Cls
			self._is2 = Is2Cls(self._core, self._cmd_group)
		return self._is2

	@property
	def isPy(self):
		"""isPy commands group. 0 Sub-classes, 17 commands."""
		if not hasattr(self, '_isPy'):
			from .IsPy import IsPyCls
			self._isPy = IsPyCls(self._core, self._cmd_group)
		return self._isPy

	@property
	def mue(self):
		"""mue commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mue'):
			from .Mue import MueCls
			self._mue = MueCls(self._core, self._cmd_group)
		return self._mue

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def rtf(self):
		"""rtf commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_rtf'):
			from .Rtf import RtfCls
			self._rtf = RtfCls(self._core, self._cmd_group)
		return self._rtf

	@property
	def sue(self):
		"""sue commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sue'):
			from .Sue import SueCls
			self._sue = SueCls(self._core, self._cmd_group)
		return self._sue

	@property
	def ws(self):
		"""ws commands group. 5 Sub-classes, 20 commands."""
		if not hasattr(self, '_ws'):
			from .Ws import WsCls
			self._ws = WsCls(self._core, self._cmd_group)
		return self._ws

	def get_bewphi(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BEWPhi \n
		Snippet: value: float = driver.source.bb.nr5G.tcw.get_bewphi() \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the phi-axis (BeWtheta,REFSENS) , applicable for FR1 only. \n
			:return: bewphi_ref_sens: float Range: 0.1 to 360
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BEWPhi?')
		return Conversions.str_to_float(response)

	def set_bewphi(self, bewphi_ref_sens: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BEWPhi \n
		Snippet: driver.source.bb.nr5G.tcw.set_bewphi(bewphi_ref_sens = 1.0) \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the phi-axis (BeWtheta,REFSENS) , applicable for FR1 only. \n
			:param bewphi_ref_sens: float Range: 0.1 to 360
		"""
		param = Conversions.decimal_value_to_str(bewphi_ref_sens)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BEWPhi {param}')

	def get_bewthet(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BEWThet \n
		Snippet: value: float = driver.source.bb.nr5G.tcw.get_bewthet() \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the theta-axis (BeWtheta,REFSENS) , applicable for FR1
		only. \n
			:return: bewthet_ref_sens: float Range: 0.1 to 360
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BEWThet?')
		return Conversions.str_to_float(response)

	def set_bewthet(self, bewthet_ref_sens: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BEWThet \n
		Snippet: driver.source.bb.nr5G.tcw.set_bewthet(bewthet_ref_sens = 1.0) \n
		Sets the angle of the beamwidth for to the OTA REFSENS RoAoA in the theta-axis (BeWtheta,REFSENS) , applicable for FR1
		only. \n
			:param bewthet_ref_sens: float Range: 0.1 to 360
		"""
		param = Conversions.decimal_value_to_str(bewthet_ref_sens)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BEWThet {param}')

	# noinspection PyTypeChecker
	def get_bs_class(self) -> enums.BsClass:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BSCLass \n
		Snippet: value: enums.BsClass = driver.source.bb.nr5G.tcw.get_bs_class() \n
		Sets the NR base station class. \n
			:return: bs_class: WIDE| MED| LOC
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BSCLass?')
		return Conversions.str_to_scalar_enum(response, enums.BsClass)

	def set_bs_class(self, bs_class: enums.BsClass) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BSCLass \n
		Snippet: driver.source.bb.nr5G.tcw.set_bs_class(bs_class = enums.BsClass.LOC) \n
		Sets the NR base station class. \n
			:param bs_class: WIDE| MED| LOC
		"""
		param = Conversions.enum_scalar_to_str(bs_class, enums.BsClass)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BSCLass {param}')

	# noinspection PyTypeChecker
	def get_bs_type(self) -> enums.BsType:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BSTYpe \n
		Snippet: value: enums.BsType = driver.source.bb.nr5G.tcw.get_bs_type() \n
		Sets the base station type for the OTA settings as specified in D.5. \n
			:return: bs_type: BT1H| BT1O| BT2O BT1 Sets the BS type 1-H (FR1, hybrid) for the OTA settings. BT1O Sets the BS type 1-O (FR1) for the OTA settings. BT2O Sets the BS type 2-O (FR2) for the OTA settings.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:BSTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BsType)

	def set_bs_type(self, bs_type: enums.BsType) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:BSTYpe \n
		Snippet: driver.source.bb.nr5G.tcw.set_bs_type(bs_type = enums.BsType.BT1H) \n
		Sets the base station type for the OTA settings as specified in D.5. \n
			:param bs_type: BT1H| BT1O| BT2O BT1 Sets the BS type 1-H (FR1, hybrid) for the OTA settings. BT1O Sets the BS type 1-O (FR1) for the OTA settings. BT2O Sets the BS type 2-O (FR2) for the OTA settings.
		"""
		param = Conversions.enum_scalar_to_str(bs_type, enums.BsType)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:BSTYpe {param}')

	# noinspection PyTypeChecker
	def get_dcl_direction(self) -> enums.DeclaredDir:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:DCLDirection \n
		Snippet: value: enums.DeclaredDir = driver.source.bb.nr5G.tcw.get_dcl_direction() \n
		Sets the reference for the OSDD. \n
			:return: declared_dir: OTHD| MREFD| OREFD OTHD Sets a value different than the minSENS and REFSENS as the reference for the OSDD. MREFD Sets the OTA minimum sensitivity (minSENS) value as the reference for the OSDD. OREFD Sets the OTA reference sensitivity (REFSENS) value as the reference for the OSDD.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:DCLDirection?')
		return Conversions.str_to_scalar_enum(response, enums.DeclaredDir)

	def set_dcl_direction(self, declared_dir: enums.DeclaredDir) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:DCLDirection \n
		Snippet: driver.source.bb.nr5G.tcw.set_dcl_direction(declared_dir = enums.DeclaredDir.MREFD) \n
		Sets the reference for the OSDD. \n
			:param declared_dir: OTHD| MREFD| OREFD OTHD Sets a value different than the minSENS and REFSENS as the reference for the OSDD. MREFD Sets the OTA minimum sensitivity (minSENS) value as the reference for the OSDD. OREFD Sets the OTA reference sensitivity (REFSENS) value as the reference for the OSDD.
		"""
		param = Conversions.enum_scalar_to_str(declared_dir, enums.DeclaredDir)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:DCLDirection {param}')

	def get_e_50(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:E50 \n
		Snippet: value: float = driver.source.bb.nr5G.tcw.get_e_50() \n
		Sets the EISREFSENS_50M level value applicable in the OTA REFSENS RoAoA as specified in D.28. The EISREFSENS_50M value is
		the declared OTA reference sensitivity basis level for FR2 based on a reference measurement channel with 50MHz BS channel
		bandwidth. \n
			:return: eis_50_m: float Range: -119 to -86
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:E50?')
		return Conversions.str_to_float(response)

	def set_e_50(self, eis_50_m: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:E50 \n
		Snippet: driver.source.bb.nr5G.tcw.set_e_50(eis_50_m = 1.0) \n
		Sets the EISREFSENS_50M level value applicable in the OTA REFSENS RoAoA as specified in D.28. The EISREFSENS_50M value is
		the declared OTA reference sensitivity basis level for FR2 based on a reference measurement channel with 50MHz BS channel
		bandwidth. \n
			:param eis_50_m: float Range: -119 to -86
		"""
		param = Conversions.decimal_value_to_str(eis_50_m)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:E50 {param}')

	# noinspection PyTypeChecker
	def get_fr(self) -> enums.FreqRange:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:FR \n
		Snippet: value: enums.FreqRange = driver.source.bb.nr5G.tcw.get_fr() \n
		No command help available \n
			:return: freq_range: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:FR?')
		return Conversions.str_to_scalar_enum(response, enums.FreqRange)

	def set_fr(self, freq_range: enums.FreqRange) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:FR \n
		Snippet: driver.source.bb.nr5G.tcw.set_fr(freq_range = enums.FreqRange.FR2GT37) \n
		No command help available \n
			:param freq_range: No help available
		"""
		param = Conversions.enum_scalar_to_str(freq_range, enums.FreqRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:FR {param}')

	# noinspection PyTypeChecker
	def get_gen_signal(self) -> enums.GenSig:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:GENSignal \n
		Snippet: value: enums.GenSig = driver.source.bb.nr5G.tcw.get_gen_signal() \n
		Selects the generated signal. \n
			:return: generated_signal: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:GENSignal?')
		return Conversions.str_to_scalar_enum(response, enums.GenSig)

	def set_gen_signal(self, generated_signal: enums.GenSig) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:GENSignal \n
		Snippet: driver.source.bb.nr5G.tcw.set_gen_signal(generated_signal = enums.GenSig.ALL) \n
		Selects the generated signal. \n
			:param generated_signal: ALL Generates both the wanted and the interferer signal. IF Generates only the interferer signal. WS Generates only the wanted signal.
		"""
		param = Conversions.enum_scalar_to_str(generated_signal, enums.GenSig)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:GENSignal {param}')

	# noinspection PyTypeChecker
	def get_inst_setup(self) -> enums.InstSetup:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:INSTsetup \n
		Snippet: value: enums.InstSetup = driver.source.bb.nr5G.tcw.get_inst_setup() \n
		No command help available \n
			:return: inst_setup: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:INSTsetup?')
		return Conversions.str_to_scalar_enum(response, enums.InstSetup)

	def set_inst_setup(self, inst_setup: enums.InstSetup) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:INSTsetup \n
		Snippet: driver.source.bb.nr5G.tcw.set_inst_setup(inst_setup = enums.InstSetup.U1PORT) \n
		No command help available \n
			:param inst_setup: No help available
		"""
		param = Conversions.enum_scalar_to_str(inst_setup, enums.InstSetup)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:INSTsetup {param}')

	# noinspection PyTypeChecker
	def get_marker_config(self) -> enums.MarkConf:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:MARKerconfig \n
		Snippet: value: enums.MarkConf = driver.source.bb.nr5G.tcw.get_marker_config() \n
		Selects the marker configuration. The marker can be used to synchronize the measuring equipment to the signal generator. \n
			:return: marker_config: FRAM| UNCH FRAM The marker settings are customized for the selected test case. 'Radio Frame Start' markers are output; the marker delays are set equal to zero. UNCH The current marker settings of the signal generator are retained unchanged.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:MARKerconfig?')
		return Conversions.str_to_scalar_enum(response, enums.MarkConf)

	def set_marker_config(self, marker_config: enums.MarkConf) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:MARKerconfig \n
		Snippet: driver.source.bb.nr5G.tcw.set_marker_config(marker_config = enums.MarkConf.FRAM) \n
		Selects the marker configuration. The marker can be used to synchronize the measuring equipment to the signal generator. \n
			:param marker_config: FRAM| UNCH FRAM The marker settings are customized for the selected test case. 'Radio Frame Start' markers are output; the marker delays are set equal to zero. UNCH The current marker settings of the signal generator are retained unchanged.
		"""
		param = Conversions.enum_scalar_to_str(marker_config, enums.MarkConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:MARKerconfig {param}')

	def get_meis(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:MEIS \n
		Snippet: value: float = driver.source.bb.nr5G.tcw.get_meis() \n
		Sets the lowest equivalent isotropic sensitivity value (EISminSENS) for the OSDD as specified in D.27. \n
			:return: minimum_eis: float Range: -145 to -10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:MEIS?')
		return Conversions.str_to_float(response)

	def set_meis(self, minimum_eis: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:MEIS \n
		Snippet: driver.source.bb.nr5G.tcw.set_meis(minimum_eis = 1.0) \n
		Sets the lowest equivalent isotropic sensitivity value (EISminSENS) for the OSDD as specified in D.27. \n
			:param minimum_eis: float Range: -145 to -10
		"""
		param = Conversions.decimal_value_to_str(minimum_eis)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:MEIS {param}')

	def get_opt_str(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:OPTStr \n
		Snippet: value: str = driver.source.bb.nr5G.tcw.get_opt_str() \n
		No command help available \n
			:return: option_str: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:OPTStr?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_release(self) -> enums.Release:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:RELease \n
		Snippet: value: enums.Release = driver.source.bb.nr5G.tcw.get_release() \n
		Sets the 3GPP test specification used as a guideline for the test cases. \n
			:return: release: REL15| REL16| REL17
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:RELease?')
		return Conversions.str_to_scalar_enum(response, enums.Release)

	def set_release(self, release: enums.Release) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:RELease \n
		Snippet: driver.source.bb.nr5G.tcw.set_release(release = enums.Release.REL15) \n
		Sets the 3GPP test specification used as a guideline for the test cases. \n
			:param release: REL15| REL16| REL17
		"""
		param = Conversions.enum_scalar_to_str(release, enums.Release)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:RELease {param}')

	# noinspection PyTypeChecker
	def get_spec(self) -> enums.TestSpec:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:SPEC \n
		Snippet: value: enums.TestSpec = driver.source.bb.nr5G.tcw.get_spec() \n
		Specifies the 3GPP test specification. \n
			:return: test_spec: TS38141_1| TS38141_2| TS38104
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:SPEC?')
		return Conversions.str_to_scalar_enum(response, enums.TestSpec)

	def set_spec(self, test_spec: enums.TestSpec) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:SPEC \n
		Snippet: driver.source.bb.nr5G.tcw.set_spec(test_spec = enums.TestSpec.TS38104) \n
		Specifies the 3GPP test specification. \n
			:param test_spec: TS38141_1| TS38141_2| TS38104
		"""
		param = Conversions.enum_scalar_to_str(test_spec, enums.TestSpec)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:SPEC {param}')

	# noinspection PyTypeChecker
	def get_tc(self) -> enums.TestCase:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:TC \n
		Snippet: value: enums.TestCase = driver.source.bb.nr5G.tcw.get_tc() \n
		Selects the test case. \n
			:return: test_case: TS381411_TC72| TS381411_TC73| TS381411_TC741| TS381411_TC742A| TS381411_TC742B| TS381411_TC75| TS381411_TC77| TS381411_TC78| TS381411_TC821| TS381411_TC822| TS381411_TC823| TS381411_TC831| TS381411_TC8321| TS381411_TC8322| TS381411_TC8331| TS381411_TC8332| TS381411_TC834| TS381411_TC835| TS381411_TC8361A| TS381411_TC8361B| TS381411_TC841| TS381411_TC67| TS381412_TC72| TS381412_TC73| TS381412_TC74| TS381412_TC751| TS381412_TC752A| TS381412_TC752B| TS381412_TC76| TS381412_TC78| TS381412_TC79| TS381412_TC821| TS381412_TC822| TS381412_TC823| TS381412_TC831| TS381412_TC8321| TS381412_TC8322| TS381412_TC8331| TS381412_TC8332| TS381412_TC834| TS381412_TC835| TS381412_TC8361A| TS381412_TC8361B| TS381412_TC841| TS381412_TC68| TS381411_TC824| TS381411_TC825| TS381411_TC826| TS381411_TC827| TS381411_TC828| TS381411_TC829| TS381412_TC824| TS381412_TC825| TS381412_TC826| TS381412_TC827| TS381412_TC828| TS381412_TC829| TS381411_TC8210| TS381412_TC8210| TS381411_TC8211| TS381412_TC8211| TS381411_TC837| TS381412_TC837| TS381411_TC8381| TS381412_TC8381| TS381411_TC8382| TS381412_TC8382| TS381411_TC839| TS381412_TC839| TS381411_TC8310| TS381412_TC8310| TS381411_TC8212| TS381412_TC8212| TS381411_TC8213| TS381412_TC8213| TS381411_TC8311| TS381412_TC8311| TS381411_TC83122| TS381411_TC83121| TS381412_TC83121| TS381411_TC8313| TS381412_TC83122| TS381412_TC8313 The first part of the parameter indicates the standard document and the second part the chapter in which the test case is defined. For example, TS381411_TC72 defines the test case specified in chapter 7.2.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:TC?')
		return Conversions.str_to_scalar_enum(response, enums.TestCase)

	def set_tc(self, test_case: enums.TestCase) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:TC \n
		Snippet: driver.source.bb.nr5G.tcw.set_tc(test_case = enums.TestCase.TS381411_TC67) \n
		Selects the test case. \n
			:param test_case: TS381411_TC72| TS381411_TC73| TS381411_TC741| TS381411_TC742A| TS381411_TC742B| TS381411_TC75| TS381411_TC77| TS381411_TC78| TS381411_TC821| TS381411_TC822| TS381411_TC823| TS381411_TC831| TS381411_TC8321| TS381411_TC8322| TS381411_TC8331| TS381411_TC8332| TS381411_TC834| TS381411_TC835| TS381411_TC8361A| TS381411_TC8361B| TS381411_TC841| TS381411_TC67| TS381412_TC72| TS381412_TC73| TS381412_TC74| TS381412_TC751| TS381412_TC752A| TS381412_TC752B| TS381412_TC76| TS381412_TC78| TS381412_TC79| TS381412_TC821| TS381412_TC822| TS381412_TC823| TS381412_TC831| TS381412_TC8321| TS381412_TC8322| TS381412_TC8331| TS381412_TC8332| TS381412_TC834| TS381412_TC835| TS381412_TC8361A| TS381412_TC8361B| TS381412_TC841| TS381412_TC68| TS381411_TC824| TS381411_TC825| TS381411_TC826| TS381411_TC827| TS381411_TC828| TS381411_TC829| TS381412_TC824| TS381412_TC825| TS381412_TC826| TS381412_TC827| TS381412_TC828| TS381412_TC829| TS381411_TC8210| TS381412_TC8210| TS381411_TC8211| TS381412_TC8211| TS381411_TC837| TS381412_TC837| TS381411_TC8381| TS381412_TC8381| TS381411_TC8382| TS381412_TC8382| TS381411_TC839| TS381412_TC839| TS381411_TC8310| TS381412_TC8310| TS381411_TC8212| TS381412_TC8212| TS381411_TC8213| TS381412_TC8213| TS381411_TC8311| TS381412_TC8311| TS381411_TC83122| TS381411_TC83121| TS381412_TC83121| TS381411_TC8313| TS381412_TC83122| TS381412_TC8313 The first part of the parameter indicates the standard document and the second part the chapter in which the test case is defined. For example, TS381411_TC72 defines the test case specified in chapter 7.2.
		"""
		param = Conversions.enum_scalar_to_str(test_case, enums.TestCase)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:TC {param}')

	# noinspection PyTypeChecker
	def get_trigger_config(self) -> enums.TrigConf:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:TRIGgerconfig \n
		Snippet: value: enums.TrigConf = driver.source.bb.nr5G.tcw.get_trigger_config() \n
		Selects the trigger configuration. The trigger is used to synchronize the signal generator to the other equipment. \n
			:return: trig_config: AAUT| UNCH AAUT The trigger settings are customized for the selected test case. The trigger setting 'Armed Auto' with external trigger source is used; the trigger delay is set to zero. Thus, the base station frame timing is able to synchronize the signal generator by a periodic trigger. UNCH The current trigger settings of the signal generator are retained unchanged.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:TRIGgerconfig?')
		return Conversions.str_to_scalar_enum(response, enums.TrigConf)

	def set_trigger_config(self, trig_config: enums.TrigConf) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:TRIGgerconfig \n
		Snippet: driver.source.bb.nr5G.tcw.set_trigger_config(trig_config = enums.TrigConf.AAUT) \n
		Selects the trigger configuration. The trigger is used to synchronize the signal generator to the other equipment. \n
			:param trig_config: AAUT| UNCH AAUT The trigger settings are customized for the selected test case. The trigger setting 'Armed Auto' with external trigger source is used; the trigger delay is set to zero. Thus, the base station frame timing is able to synchronize the signal generator by a periodic trigger. UNCH The current trigger settings of the signal generator are retained unchanged.
		"""
		param = Conversions.enum_scalar_to_str(trig_config, enums.TrigConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:TRIGgerconfig {param}')

	def clone(self) -> 'TcwCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TcwCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
