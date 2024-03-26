from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DciCls:
	"""Dci commands group definition. 272 total commands, 268 Subgroups, 0 group commands
	Repeated Capability: IndexNull, default value after init: IndexNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dci", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_indexNull_get', 'repcap_indexNull_set', repcap.IndexNull.Nr0)

	def repcap_indexNull_set(self, indexNull: repcap.IndexNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IndexNull.Default
		Default value after init: IndexNull.Nr0"""
		self._cmd_group.set_repcap_enum_value(indexNull)

	def repcap_indexNull_get(self) -> repcap.IndexNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def aggLevel(self):
		"""aggLevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aggLevel'):
			from .AggLevel import AggLevelCls
			self._aggLevel = AggLevelCls(self._core, self._cmd_group)
		return self._aggLevel

	@property
	def ai1(self):
		"""ai1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai1'):
			from .Ai1 import Ai1Cls
			self._ai1 = Ai1Cls(self._core, self._cmd_group)
		return self._ai1

	@property
	def ai10(self):
		"""ai10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai10'):
			from .Ai10 import Ai10Cls
			self._ai10 = Ai10Cls(self._core, self._cmd_group)
		return self._ai10

	@property
	def ai11(self):
		"""ai11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai11'):
			from .Ai11 import Ai11Cls
			self._ai11 = Ai11Cls(self._core, self._cmd_group)
		return self._ai11

	@property
	def ai12(self):
		"""ai12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai12'):
			from .Ai12 import Ai12Cls
			self._ai12 = Ai12Cls(self._core, self._cmd_group)
		return self._ai12

	@property
	def ai13(self):
		"""ai13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai13'):
			from .Ai13 import Ai13Cls
			self._ai13 = Ai13Cls(self._core, self._cmd_group)
		return self._ai13

	@property
	def ai14(self):
		"""ai14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai14'):
			from .Ai14 import Ai14Cls
			self._ai14 = Ai14Cls(self._core, self._cmd_group)
		return self._ai14

	@property
	def ai15(self):
		"""ai15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai15'):
			from .Ai15 import Ai15Cls
			self._ai15 = Ai15Cls(self._core, self._cmd_group)
		return self._ai15

	@property
	def ai16(self):
		"""ai16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai16'):
			from .Ai16 import Ai16Cls
			self._ai16 = Ai16Cls(self._core, self._cmd_group)
		return self._ai16

	@property
	def ai2(self):
		"""ai2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai2'):
			from .Ai2 import Ai2Cls
			self._ai2 = Ai2Cls(self._core, self._cmd_group)
		return self._ai2

	@property
	def ai3(self):
		"""ai3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai3'):
			from .Ai3 import Ai3Cls
			self._ai3 = Ai3Cls(self._core, self._cmd_group)
		return self._ai3

	@property
	def ai4(self):
		"""ai4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai4'):
			from .Ai4 import Ai4Cls
			self._ai4 = Ai4Cls(self._core, self._cmd_group)
		return self._ai4

	@property
	def ai5(self):
		"""ai5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai5'):
			from .Ai5 import Ai5Cls
			self._ai5 = Ai5Cls(self._core, self._cmd_group)
		return self._ai5

	@property
	def ai6(self):
		"""ai6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai6'):
			from .Ai6 import Ai6Cls
			self._ai6 = Ai6Cls(self._core, self._cmd_group)
		return self._ai6

	@property
	def ai7(self):
		"""ai7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai7'):
			from .Ai7 import Ai7Cls
			self._ai7 = Ai7Cls(self._core, self._cmd_group)
		return self._ai7

	@property
	def ai8(self):
		"""ai8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai8'):
			from .Ai8 import Ai8Cls
			self._ai8 = Ai8Cls(self._core, self._cmd_group)
		return self._ai8

	@property
	def ai9(self):
		"""ai9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai9'):
			from .Ai9 import Ai9Cls
			self._ai9 = Ai9Cls(self._core, self._cmd_group)
		return self._ai9

	@property
	def antPorts(self):
		"""antPorts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_antPorts'):
			from .AntPorts import AntPortsCls
			self._antPorts = AntPortsCls(self._core, self._cmd_group)
		return self._antPorts

	@property
	def ar1(self):
		"""ar1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar1'):
			from .Ar1 import Ar1Cls
			self._ar1 = Ar1Cls(self._core, self._cmd_group)
		return self._ar1

	@property
	def ar10(self):
		"""ar10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar10'):
			from .Ar10 import Ar10Cls
			self._ar10 = Ar10Cls(self._core, self._cmd_group)
		return self._ar10

	@property
	def ar11(self):
		"""ar11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar11'):
			from .Ar11 import Ar11Cls
			self._ar11 = Ar11Cls(self._core, self._cmd_group)
		return self._ar11

	@property
	def ar12(self):
		"""ar12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar12'):
			from .Ar12 import Ar12Cls
			self._ar12 = Ar12Cls(self._core, self._cmd_group)
		return self._ar12

	@property
	def ar13(self):
		"""ar13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar13'):
			from .Ar13 import Ar13Cls
			self._ar13 = Ar13Cls(self._core, self._cmd_group)
		return self._ar13

	@property
	def ar14(self):
		"""ar14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar14'):
			from .Ar14 import Ar14Cls
			self._ar14 = Ar14Cls(self._core, self._cmd_group)
		return self._ar14

	@property
	def ar15(self):
		"""ar15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar15'):
			from .Ar15 import Ar15Cls
			self._ar15 = Ar15Cls(self._core, self._cmd_group)
		return self._ar15

	@property
	def ar16(self):
		"""ar16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar16'):
			from .Ar16 import Ar16Cls
			self._ar16 = Ar16Cls(self._core, self._cmd_group)
		return self._ar16

	@property
	def ar2(self):
		"""ar2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar2'):
			from .Ar2 import Ar2Cls
			self._ar2 = Ar2Cls(self._core, self._cmd_group)
		return self._ar2

	@property
	def ar3(self):
		"""ar3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar3'):
			from .Ar3 import Ar3Cls
			self._ar3 = Ar3Cls(self._core, self._cmd_group)
		return self._ar3

	@property
	def ar4(self):
		"""ar4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar4'):
			from .Ar4 import Ar4Cls
			self._ar4 = Ar4Cls(self._core, self._cmd_group)
		return self._ar4

	@property
	def ar5(self):
		"""ar5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar5'):
			from .Ar5 import Ar5Cls
			self._ar5 = Ar5Cls(self._core, self._cmd_group)
		return self._ar5

	@property
	def ar6(self):
		"""ar6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar6'):
			from .Ar6 import Ar6Cls
			self._ar6 = Ar6Cls(self._core, self._cmd_group)
		return self._ar6

	@property
	def ar7(self):
		"""ar7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar7'):
			from .Ar7 import Ar7Cls
			self._ar7 = Ar7Cls(self._core, self._cmd_group)
		return self._ar7

	@property
	def ar8(self):
		"""ar8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar8'):
			from .Ar8 import Ar8Cls
			self._ar8 = Ar8Cls(self._core, self._cmd_group)
		return self._ar8

	@property
	def ar9(self):
		"""ar9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ar9'):
			from .Ar9 import Ar9Cls
			self._ar9 = Ar9Cls(self._core, self._cmd_group)
		return self._ar9

	@property
	def arind(self):
		"""arind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_arind'):
			from .Arind import ArindCls
			self._arind = ArindCls(self._core, self._cmd_group)
		return self._arind

	@property
	def bitLength(self):
		"""bitLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitLength'):
			from .BitLength import BitLengthCls
			self._bitLength = BitLengthCls(self._core, self._cmd_group)
		return self._bitLength

	@property
	def boind(self):
		"""boind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_boind'):
			from .Boind import BoindCls
			self._boind = BoindCls(self._core, self._cmd_group)
		return self._boind

	@property
	def bwind(self):
		"""bwind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bwind'):
			from .Bwind import BwindCls
			self._bwind = BwindCls(self._core, self._cmd_group)
		return self._bwind

	@property
	def caCpext(self):
		"""caCpext commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caCpext'):
			from .CaCpext import CaCpextCls
			self._caCpext = CaCpextCls(self._core, self._cmd_group)
		return self._caCpext

	@property
	def caind(self):
		"""caind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caind'):
			from .Caind import CaindCls
			self._caind = CaindCls(self._core, self._cmd_group)
		return self._caind

	@property
	def caIndex(self):
		"""caIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caIndex'):
			from .CaIndex import CaIndexCls
			self._caIndex = CaIndexCls(self._core, self._cmd_group)
		return self._caIndex

	@property
	def candidate(self):
		"""candidate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_candidate'):
			from .Candidate import CandidateCls
			self._candidate = CandidateCls(self._core, self._cmd_group)
		return self._candidate

	@property
	def cbgfi(self):
		"""cbgfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbgfi'):
			from .Cbgfi import CbgfiCls
			self._cbgfi = CbgfiCls(self._core, self._cmd_group)
		return self._cbgfi

	@property
	def cbgti(self):
		"""cbgti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbgti'):
			from .Cbgti import CbgtiCls
			self._cbgti = CbgtiCls(self._core, self._cmd_group)
		return self._cbgti

	@property
	def cd1(self):
		"""cd1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd1'):
			from .Cd1 import Cd1Cls
			self._cd1 = Cd1Cls(self._core, self._cmd_group)
		return self._cd1

	@property
	def cd10(self):
		"""cd10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd10'):
			from .Cd10 import Cd10Cls
			self._cd10 = Cd10Cls(self._core, self._cmd_group)
		return self._cd10

	@property
	def cd11(self):
		"""cd11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd11'):
			from .Cd11 import Cd11Cls
			self._cd11 = Cd11Cls(self._core, self._cmd_group)
		return self._cd11

	@property
	def cd12(self):
		"""cd12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd12'):
			from .Cd12 import Cd12Cls
			self._cd12 = Cd12Cls(self._core, self._cmd_group)
		return self._cd12

	@property
	def cd13(self):
		"""cd13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd13'):
			from .Cd13 import Cd13Cls
			self._cd13 = Cd13Cls(self._core, self._cmd_group)
		return self._cd13

	@property
	def cd14(self):
		"""cd14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd14'):
			from .Cd14 import Cd14Cls
			self._cd14 = Cd14Cls(self._core, self._cmd_group)
		return self._cd14

	@property
	def cd15(self):
		"""cd15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd15'):
			from .Cd15 import Cd15Cls
			self._cd15 = Cd15Cls(self._core, self._cmd_group)
		return self._cd15

	@property
	def cd16(self):
		"""cd16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd16'):
			from .Cd16 import Cd16Cls
			self._cd16 = Cd16Cls(self._core, self._cmd_group)
		return self._cd16

	@property
	def cd2(self):
		"""cd2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd2'):
			from .Cd2 import Cd2Cls
			self._cd2 = Cd2Cls(self._core, self._cmd_group)
		return self._cd2

	@property
	def cd3(self):
		"""cd3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd3'):
			from .Cd3 import Cd3Cls
			self._cd3 = Cd3Cls(self._core, self._cmd_group)
		return self._cd3

	@property
	def cd4(self):
		"""cd4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd4'):
			from .Cd4 import Cd4Cls
			self._cd4 = Cd4Cls(self._core, self._cmd_group)
		return self._cd4

	@property
	def cd5(self):
		"""cd5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd5'):
			from .Cd5 import Cd5Cls
			self._cd5 = Cd5Cls(self._core, self._cmd_group)
		return self._cd5

	@property
	def cd6(self):
		"""cd6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd6'):
			from .Cd6 import Cd6Cls
			self._cd6 = Cd6Cls(self._core, self._cmd_group)
		return self._cd6

	@property
	def cd7(self):
		"""cd7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd7'):
			from .Cd7 import Cd7Cls
			self._cd7 = Cd7Cls(self._core, self._cmd_group)
		return self._cd7

	@property
	def cd8(self):
		"""cd8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd8'):
			from .Cd8 import Cd8Cls
			self._cd8 = Cd8Cls(self._core, self._cmd_group)
		return self._cd8

	@property
	def cd9(self):
		"""cd9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cd9'):
			from .Cd9 import Cd9Cls
			self._cd9 = Cd9Cls(self._core, self._cmd_group)
		return self._cd9

	@property
	def ci10(self):
		"""ci10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci10'):
			from .Ci10 import Ci10Cls
			self._ci10 = Ci10Cls(self._core, self._cmd_group)
		return self._ci10

	@property
	def ci11(self):
		"""ci11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci11'):
			from .Ci11 import Ci11Cls
			self._ci11 = Ci11Cls(self._core, self._cmd_group)
		return self._ci11

	@property
	def ci12(self):
		"""ci12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci12'):
			from .Ci12 import Ci12Cls
			self._ci12 = Ci12Cls(self._core, self._cmd_group)
		return self._ci12

	@property
	def ci13(self):
		"""ci13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci13'):
			from .Ci13 import Ci13Cls
			self._ci13 = Ci13Cls(self._core, self._cmd_group)
		return self._ci13

	@property
	def ci14(self):
		"""ci14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci14'):
			from .Ci14 import Ci14Cls
			self._ci14 = Ci14Cls(self._core, self._cmd_group)
		return self._ci14

	@property
	def ci15(self):
		"""ci15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci15'):
			from .Ci15 import Ci15Cls
			self._ci15 = Ci15Cls(self._core, self._cmd_group)
		return self._ci15

	@property
	def ci16(self):
		"""ci16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci16'):
			from .Ci16 import Ci16Cls
			self._ci16 = Ci16Cls(self._core, self._cmd_group)
		return self._ci16

	@property
	def ci2(self):
		"""ci2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci2'):
			from .Ci2 import Ci2Cls
			self._ci2 = Ci2Cls(self._core, self._cmd_group)
		return self._ci2

	@property
	def ci3(self):
		"""ci3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci3'):
			from .Ci3 import Ci3Cls
			self._ci3 = Ci3Cls(self._core, self._cmd_group)
		return self._ci3

	@property
	def ci4(self):
		"""ci4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci4'):
			from .Ci4 import Ci4Cls
			self._ci4 = Ci4Cls(self._core, self._cmd_group)
		return self._ci4

	@property
	def ci5(self):
		"""ci5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci5'):
			from .Ci5 import Ci5Cls
			self._ci5 = Ci5Cls(self._core, self._cmd_group)
		return self._ci5

	@property
	def ci6(self):
		"""ci6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci6'):
			from .Ci6 import Ci6Cls
			self._ci6 = Ci6Cls(self._core, self._cmd_group)
		return self._ci6

	@property
	def ci7(self):
		"""ci7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci7'):
			from .Ci7 import Ci7Cls
			self._ci7 = Ci7Cls(self._core, self._cmd_group)
		return self._ci7

	@property
	def ci8(self):
		"""ci8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci8'):
			from .Ci8 import Ci8Cls
			self._ci8 = Ci8Cls(self._core, self._cmd_group)
		return self._ci8

	@property
	def ci9(self):
		"""ci9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci9'):
			from .Ci9 import Ci9Cls
			self._ci9 = Ci9Cls(self._core, self._cmd_group)
		return self._ci9

	@property
	def cl1(self):
		"""cl1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl1'):
			from .Cl1 import Cl1Cls
			self._cl1 = Cl1Cls(self._core, self._cmd_group)
		return self._cl1

	@property
	def cl10(self):
		"""cl10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl10'):
			from .Cl10 import Cl10Cls
			self._cl10 = Cl10Cls(self._core, self._cmd_group)
		return self._cl10

	@property
	def cl11(self):
		"""cl11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl11'):
			from .Cl11 import Cl11Cls
			self._cl11 = Cl11Cls(self._core, self._cmd_group)
		return self._cl11

	@property
	def cl12(self):
		"""cl12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl12'):
			from .Cl12 import Cl12Cls
			self._cl12 = Cl12Cls(self._core, self._cmd_group)
		return self._cl12

	@property
	def cl13(self):
		"""cl13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl13'):
			from .Cl13 import Cl13Cls
			self._cl13 = Cl13Cls(self._core, self._cmd_group)
		return self._cl13

	@property
	def cl14(self):
		"""cl14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl14'):
			from .Cl14 import Cl14Cls
			self._cl14 = Cl14Cls(self._core, self._cmd_group)
		return self._cl14

	@property
	def cl15(self):
		"""cl15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl15'):
			from .Cl15 import Cl15Cls
			self._cl15 = Cl15Cls(self._core, self._cmd_group)
		return self._cl15

	@property
	def cl16(self):
		"""cl16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl16'):
			from .Cl16 import Cl16Cls
			self._cl16 = Cl16Cls(self._core, self._cmd_group)
		return self._cl16

	@property
	def cl17(self):
		"""cl17 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl17'):
			from .Cl17 import Cl17Cls
			self._cl17 = Cl17Cls(self._core, self._cmd_group)
		return self._cl17

	@property
	def cl18(self):
		"""cl18 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl18'):
			from .Cl18 import Cl18Cls
			self._cl18 = Cl18Cls(self._core, self._cmd_group)
		return self._cl18

	@property
	def cl19(self):
		"""cl19 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl19'):
			from .Cl19 import Cl19Cls
			self._cl19 = Cl19Cls(self._core, self._cmd_group)
		return self._cl19

	@property
	def cl2(self):
		"""cl2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl2'):
			from .Cl2 import Cl2Cls
			self._cl2 = Cl2Cls(self._core, self._cmd_group)
		return self._cl2

	@property
	def cl20(self):
		"""cl20 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl20'):
			from .Cl20 import Cl20Cls
			self._cl20 = Cl20Cls(self._core, self._cmd_group)
		return self._cl20

	@property
	def cl21(self):
		"""cl21 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl21'):
			from .Cl21 import Cl21Cls
			self._cl21 = Cl21Cls(self._core, self._cmd_group)
		return self._cl21

	@property
	def cl22(self):
		"""cl22 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl22'):
			from .Cl22 import Cl22Cls
			self._cl22 = Cl22Cls(self._core, self._cmd_group)
		return self._cl22

	@property
	def cl3(self):
		"""cl3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl3'):
			from .Cl3 import Cl3Cls
			self._cl3 = Cl3Cls(self._core, self._cmd_group)
		return self._cl3

	@property
	def cl4(self):
		"""cl4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl4'):
			from .Cl4 import Cl4Cls
			self._cl4 = Cl4Cls(self._core, self._cmd_group)
		return self._cl4

	@property
	def cl5(self):
		"""cl5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl5'):
			from .Cl5 import Cl5Cls
			self._cl5 = Cl5Cls(self._core, self._cmd_group)
		return self._cl5

	@property
	def cl6(self):
		"""cl6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl6'):
			from .Cl6 import Cl6Cls
			self._cl6 = Cl6Cls(self._core, self._cmd_group)
		return self._cl6

	@property
	def cl7(self):
		"""cl7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl7'):
			from .Cl7 import Cl7Cls
			self._cl7 = Cl7Cls(self._core, self._cmd_group)
		return self._cl7

	@property
	def cl8(self):
		"""cl8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl8'):
			from .Cl8 import Cl8Cls
			self._cl8 = Cl8Cls(self._core, self._cmd_group)
		return self._cl8

	@property
	def cl9(self):
		"""cl9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl9'):
			from .Cl9 import Cl9Cls
			self._cl9 = Cl9Cls(self._core, self._cmd_group)
		return self._cl9

	@property
	def coIndex(self):
		"""coIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coIndex'):
			from .CoIndex import CoIndexCls
			self._coIndex = CoIndexCls(self._core, self._cmd_group)
		return self._coIndex

	@property
	def cpdsch(self):
		"""cpdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpdsch'):
			from .Cpdsch import CpdschCls
			self._cpdsch = CpdschCls(self._core, self._cmd_group)
		return self._cpdsch

	@property
	def csiRequest(self):
		"""csiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiRequest'):
			from .CsiRequest import CsiRequestCls
			self._csiRequest = CsiRequestCls(self._core, self._cmd_group)
		return self._csiRequest

	@property
	def dai1(self):
		"""dai1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dai1'):
			from .Dai1 import Dai1Cls
			self._dai1 = Dai1Cls(self._core, self._cmd_group)
		return self._dai1

	@property
	def dai2(self):
		"""dai2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dai2'):
			from .Dai2 import Dai2Cls
			self._dai2 = Dai2Cls(self._core, self._cmd_group)
		return self._dai2

	@property
	def dai3(self):
		"""dai3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dai3'):
			from .Dai3 import Dai3Cls
			self._dai3 = Dai3Cls(self._core, self._cmd_group)
		return self._dai3

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def dfiFlag(self):
		"""dfiFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfiFlag'):
			from .DfiFlag import DfiFlagCls
			self._dfiFlag = DfiFlagCls(self._core, self._cmd_group)
		return self._dfiFlag

	@property
	def di1(self):
		"""di1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di1'):
			from .Di1 import Di1Cls
			self._di1 = Di1Cls(self._core, self._cmd_group)
		return self._di1

	@property
	def di10(self):
		"""di10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di10'):
			from .Di10 import Di10Cls
			self._di10 = Di10Cls(self._core, self._cmd_group)
		return self._di10

	@property
	def di2(self):
		"""di2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di2'):
			from .Di2 import Di2Cls
			self._di2 = Di2Cls(self._core, self._cmd_group)
		return self._di2

	@property
	def di3(self):
		"""di3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di3'):
			from .Di3 import Di3Cls
			self._di3 = Di3Cls(self._core, self._cmd_group)
		return self._di3

	@property
	def di4(self):
		"""di4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di4'):
			from .Di4 import Di4Cls
			self._di4 = Di4Cls(self._core, self._cmd_group)
		return self._di4

	@property
	def di5(self):
		"""di5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di5'):
			from .Di5 import Di5Cls
			self._di5 = Di5Cls(self._core, self._cmd_group)
		return self._di5

	@property
	def di6(self):
		"""di6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di6'):
			from .Di6 import Di6Cls
			self._di6 = Di6Cls(self._core, self._cmd_group)
		return self._di6

	@property
	def di7(self):
		"""di7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di7'):
			from .Di7 import Di7Cls
			self._di7 = Di7Cls(self._core, self._cmd_group)
		return self._di7

	@property
	def di8(self):
		"""di8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di8'):
			from .Di8 import Di8Cls
			self._di8 = Di8Cls(self._core, self._cmd_group)
		return self._di8

	@property
	def di9(self):
		"""di9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di9'):
			from .Di9 import Di9Cls
			self._di9 = Di9Cls(self._core, self._cmd_group)
		return self._di9

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .Dlist import DlistCls
			self._dlist = DlistCls(self._core, self._cmd_group)
		return self._dlist

	@property
	def dmr2(self):
		"""dmr2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmr2'):
			from .Dmr2 import Dmr2Cls
			self._dmr2 = Dmr2Cls(self._core, self._cmd_group)
		return self._dmr2

	@property
	def dmsqInit(self):
		"""dmsqInit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmsqInit'):
			from .DmsqInit import DmsqInitCls
			self._dmsqInit = DmsqInitCls(self._core, self._cmd_group)
		return self._dmsqInit

	@property
	def dmss(self):
		"""dmss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmss'):
			from .Dmss import DmssCls
			self._dmss = DmssCls(self._core, self._cmd_group)
		return self._dmss

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Fmt import FmtCls
			self._fmt = FmtCls(self._core, self._cmd_group)
		return self._fmt

	@property
	def frdRes(self):
		"""frdRes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frdRes'):
			from .FrdRes import FrdResCls
			self._frdRes = FrdResCls(self._core, self._cmd_group)
		return self._frdRes

	@property
	def frhFlag(self):
		"""frhFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frhFlag'):
			from .FrhFlag import FrhFlagCls
			self._frhFlag = FrhFlagCls(self._core, self._cmd_group)
		return self._frhFlag

	@property
	def frrLoc(self):
		"""frrLoc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frrLoc'):
			from .FrrLoc import FrrLocCls
			self._frrLoc = FrrLocCls(self._core, self._cmd_group)
		return self._frrLoc

	@property
	def fsChannel(self):
		"""fsChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fsChannel'):
			from .FsChannel import FsChannelCls
			self._fsChannel = FsChannelCls(self._core, self._cmd_group)
		return self._fsChannel

	@property
	def haaBitmap(self):
		"""haaBitmap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_haaBitmap'):
			from .HaaBitmap import HaaBitmapCls
			self._haaBitmap = HaaBitmapCls(self._core, self._cmd_group)
		return self._haaBitmap

	@property
	def hafb(self):
		"""hafb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hafb'):
			from .Hafb import HafbCls
			self._hafb = HafbCls(self._core, self._cmd_group)
		return self._hafb

	@property
	def haproc(self):
		"""haproc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_haproc'):
			from .Haproc import HaprocCls
			self._haproc = HaprocCls(self._core, self._cmd_group)
		return self._haproc

	@property
	def hartInd(self):
		"""hartInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hartInd'):
			from .HartInd import HartIndCls
			self._hartInd = HartIndCls(self._core, self._cmd_group)
		return self._hartInd

	@property
	def hqaRequest(self):
		"""hqaRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hqaRequest'):
			from .HqaRequest import HqaRequestCls
			self._hqaRequest = HqaRequestCls(self._core, self._cmd_group)
		return self._hqaRequest

	@property
	def identifier(self):
		"""identifier commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_identifier'):
			from .Identifier import IdentifierCls
			self._identifier = IdentifierCls(self._core, self._cmd_group)
		return self._identifier

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Index import IndexCls
			self._index = IndexCls(self._core, self._cmd_group)
		return self._index

	@property
	def initPattern(self):
		"""initPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_initPattern'):
			from .InitPattern import InitPatternCls
			self._initPattern = InitPatternCls(self._core, self._cmd_group)
		return self._initPattern

	@property
	def insPatt(self):
		"""insPatt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insPatt'):
			from .InsPatt import InsPattCls
			self._insPatt = InsPattCls(self._core, self._cmd_group)
		return self._insPatt

	@property
	def lsbsfn(self):
		"""lsbsfn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lsbsfn'):
			from .Lsbsfn import LsbsfnCls
			self._lsbsfn = LsbsfnCls(self._core, self._cmd_group)
		return self._lsbsfn

	@property
	def mcch(self):
		"""mcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcch'):
			from .Mcch import McchCls
			self._mcch = McchCls(self._core, self._cmd_group)
		return self._mcch

	@property
	def moffs(self):
		"""moffs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_moffs'):
			from .Moffs import MoffsCls
			self._moffs = MoffsCls(self._core, self._cmd_group)
		return self._moffs

	@property
	def mulTable(self):
		"""mulTable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mulTable'):
			from .MulTable import MulTableCls
			self._mulTable = MulTableCls(self._core, self._cmd_group)
		return self._mulTable

	@property
	def nfIndicator(self):
		"""nfIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nfIndicator'):
			from .NfIndicator import NfIndicatorCls
			self._nfIndicator = NfIndicatorCls(self._core, self._cmd_group)
		return self._nfIndicator

	@property
	def nrpGroups(self):
		"""nrpGroups commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrpGroups'):
			from .NrpGroups import NrpGroupsCls
			self._nrpGroups = NrpGroupsCls(self._core, self._cmd_group)
		return self._nrpGroups

	@property
	def olIndicator(self):
		"""olIndicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_olIndicator'):
			from .OlIndicator import OlIndicatorCls
			self._olIndicator = OlIndicatorCls(self._core, self._cmd_group)
		return self._olIndicator

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def pcInd(self):
		"""pcInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcInd'):
			from .PcInd import PcIndCls
			self._pcInd = PcIndCls(self._core, self._cmd_group)
		return self._pcInd

	@property
	def pdsharq(self):
		"""pdsharq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdsharq'):
			from .Pdsharq import PdsharqCls
			self._pdsharq = PdsharqCls(self._core, self._cmd_group)
		return self._pdsharq

	@property
	def pe1(self):
		"""pe1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe1'):
			from .Pe1 import Pe1Cls
			self._pe1 = Pe1Cls(self._core, self._cmd_group)
		return self._pe1

	@property
	def pe2(self):
		"""pe2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe2'):
			from .Pe2 import Pe2Cls
			self._pe2 = Pe2Cls(self._core, self._cmd_group)
		return self._pe2

	@property
	def pe3(self):
		"""pe3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe3'):
			from .Pe3 import Pe3Cls
			self._pe3 = Pe3Cls(self._core, self._cmd_group)
		return self._pe3

	@property
	def pe4(self):
		"""pe4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe4'):
			from .Pe4 import Pe4Cls
			self._pe4 = Pe4Cls(self._core, self._cmd_group)
		return self._pe4

	@property
	def pe5(self):
		"""pe5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe5'):
			from .Pe5 import Pe5Cls
			self._pe5 = Pe5Cls(self._core, self._cmd_group)
		return self._pe5

	@property
	def pe6(self):
		"""pe6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe6'):
			from .Pe6 import Pe6Cls
			self._pe6 = Pe6Cls(self._core, self._cmd_group)
		return self._pe6

	@property
	def pe7(self):
		"""pe7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe7'):
			from .Pe7 import Pe7Cls
			self._pe7 = Pe7Cls(self._core, self._cmd_group)
		return self._pe7

	@property
	def pe8(self):
		"""pe8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe8'):
			from .Pe8 import Pe8Cls
			self._pe8 = Pe8Cls(self._core, self._cmd_group)
		return self._pe8

	@property
	def pe9(self):
		"""pe9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe9'):
			from .Pe9 import Pe9Cls
			self._pe9 = Pe9Cls(self._core, self._cmd_group)
		return self._pe9

	@property
	def pei1(self):
		"""pei1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei1'):
			from .Pei1 import Pei1Cls
			self._pei1 = Pei1Cls(self._core, self._cmd_group)
		return self._pei1

	@property
	def pei2(self):
		"""pei2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei2'):
			from .Pei2 import Pei2Cls
			self._pei2 = Pei2Cls(self._core, self._cmd_group)
		return self._pei2

	@property
	def pei3(self):
		"""pei3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei3'):
			from .Pei3 import Pei3Cls
			self._pei3 = Pei3Cls(self._core, self._cmd_group)
		return self._pei3

	@property
	def pei4(self):
		"""pei4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei4'):
			from .Pei4 import Pei4Cls
			self._pei4 = Pei4Cls(self._core, self._cmd_group)
		return self._pei4

	@property
	def pei5(self):
		"""pei5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei5'):
			from .Pei5 import Pei5Cls
			self._pei5 = Pei5Cls(self._core, self._cmd_group)
		return self._pei5

	@property
	def pei6(self):
		"""pei6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei6'):
			from .Pei6 import Pei6Cls
			self._pei6 = Pei6Cls(self._core, self._cmd_group)
		return self._pei6

	@property
	def pei7(self):
		"""pei7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei7'):
			from .Pei7 import Pei7Cls
			self._pei7 = Pei7Cls(self._core, self._cmd_group)
		return self._pei7

	@property
	def pei8(self):
		"""pei8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pei8'):
			from .Pei8 import Pei8Cls
			self._pei8 = Pei8Cls(self._core, self._cmd_group)
		return self._pei8

	@property
	def pgIndex(self):
		"""pgIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pgIndex'):
			from .PgIndex import PgIndexCls
			self._pgIndex = PgIndexCls(self._core, self._cmd_group)
		return self._pgIndex

	@property
	def pindicator(self):
		"""pindicator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pindicator'):
			from .Pindicator import PindicatorCls
			self._pindicator = PindicatorCls(self._core, self._cmd_group)
		return self._pindicator

	@property
	def pmAdaption(self):
		"""pmAdaption commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmAdaption'):
			from .PmAdaption import PmAdaptionCls
			self._pmAdaption = PmAdaptionCls(self._core, self._cmd_group)
		return self._pmAdaption

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def prbBundling(self):
		"""prbBundling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbBundling'):
			from .PrbBundling import PrbBundlingCls
			self._prbBundling = PrbBundlingCls(self._core, self._cmd_group)
		return self._prbBundling

	@property
	def prc2(self):
		"""prc2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prc2'):
			from .Prc2 import Prc2Cls
			self._prc2 = Prc2Cls(self._core, self._cmd_group)
		return self._prc2

	@property
	def precInfo(self):
		"""precInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_precInfo'):
			from .PrecInfo import PrecInfoCls
			self._precInfo = PrecInfoCls(self._core, self._cmd_group)
		return self._precInfo

	@property
	def ptdmrs(self):
		"""ptdmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptdmrs'):
			from .Ptdmrs import PtdmrsCls
			self._ptdmrs = PtdmrsCls(self._core, self._cmd_group)
		return self._ptdmrs

	@property
	def pthFeedback(self):
		"""pthFeedback commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pthFeedback'):
			from .PthFeedback import PthFeedbackCls
			self._pthFeedback = PthFeedbackCls(self._core, self._cmd_group)
		return self._pthFeedback

	@property
	def pucresInd(self):
		"""pucresInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pucresInd'):
			from .PucresInd import PucresIndCls
			self._pucresInd = PucresIndCls(self._core, self._cmd_group)
		return self._pucresInd

	@property
	def resved(self):
		"""resved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resved'):
			from .Resved import ResvedCls
			self._resved = ResvedCls(self._core, self._cmd_group)
		return self._resved

	@property
	def rmind(self):
		"""rmind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmind'):
			from .Rmind import RmindCls
			self._rmind = RmindCls(self._core, self._cmd_group)
		return self._rmind

	@property
	def rnti(self):
		"""rnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rnti'):
			from .Rnti import RntiCls
			self._rnti = RntiCls(self._core, self._cmd_group)
		return self._rnti

	@property
	def rpIndex(self):
		"""rpIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rpIndex'):
			from .RpIndex import RpIndexCls
			self._rpIndex = RpIndexCls(self._core, self._cmd_group)
		return self._rpIndex

	@property
	def sai(self):
		"""sai commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sai'):
			from .Sai import SaiCls
			self._sai = SaiCls(self._core, self._cmd_group)
		return self._sai

	@property
	def sgs1(self):
		"""sgs1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgs1'):
			from .Sgs1 import Sgs1Cls
			self._sgs1 = Sgs1Cls(self._core, self._cmd_group)
		return self._sgs1

	@property
	def sgs2(self):
		"""sgs2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgs2'):
			from .Sgs2 import Sgs2Cls
			self._sgs2 = Sgs2Cls(self._core, self._cmd_group)
		return self._sgs2

	@property
	def sgs3(self):
		"""sgs3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgs3'):
			from .Sgs3 import Sgs3Cls
			self._sgs3 = Sgs3Cls(self._core, self._cmd_group)
		return self._sgs3

	@property
	def sgs4(self):
		"""sgs4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgs4'):
			from .Sgs4 import Sgs4Cls
			self._sgs4 = Sgs4Cls(self._core, self._cmd_group)
		return self._sgs4

	@property
	def si1(self):
		"""si1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si1'):
			from .Si1 import Si1Cls
			self._si1 = Si1Cls(self._core, self._cmd_group)
		return self._si1

	@property
	def si10(self):
		"""si10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si10'):
			from .Si10 import Si10Cls
			self._si10 = Si10Cls(self._core, self._cmd_group)
		return self._si10

	@property
	def si11(self):
		"""si11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si11'):
			from .Si11 import Si11Cls
			self._si11 = Si11Cls(self._core, self._cmd_group)
		return self._si11

	@property
	def si12(self):
		"""si12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si12'):
			from .Si12 import Si12Cls
			self._si12 = Si12Cls(self._core, self._cmd_group)
		return self._si12

	@property
	def si13(self):
		"""si13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si13'):
			from .Si13 import Si13Cls
			self._si13 = Si13Cls(self._core, self._cmd_group)
		return self._si13

	@property
	def si14(self):
		"""si14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si14'):
			from .Si14 import Si14Cls
			self._si14 = Si14Cls(self._core, self._cmd_group)
		return self._si14

	@property
	def si15(self):
		"""si15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si15'):
			from .Si15 import Si15Cls
			self._si15 = Si15Cls(self._core, self._cmd_group)
		return self._si15

	@property
	def si16(self):
		"""si16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si16'):
			from .Si16 import Si16Cls
			self._si16 = Si16Cls(self._core, self._cmd_group)
		return self._si16

	@property
	def si2(self):
		"""si2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si2'):
			from .Si2 import Si2Cls
			self._si2 = Si2Cls(self._core, self._cmd_group)
		return self._si2

	@property
	def si3(self):
		"""si3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si3'):
			from .Si3 import Si3Cls
			self._si3 = Si3Cls(self._core, self._cmd_group)
		return self._si3

	@property
	def si4(self):
		"""si4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si4'):
			from .Si4 import Si4Cls
			self._si4 = Si4Cls(self._core, self._cmd_group)
		return self._si4

	@property
	def si5(self):
		"""si5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si5'):
			from .Si5 import Si5Cls
			self._si5 = Si5Cls(self._core, self._cmd_group)
		return self._si5

	@property
	def si6(self):
		"""si6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si6'):
			from .Si6 import Si6Cls
			self._si6 = Si6Cls(self._core, self._cmd_group)
		return self._si6

	@property
	def si7(self):
		"""si7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si7'):
			from .Si7 import Si7Cls
			self._si7 = Si7Cls(self._core, self._cmd_group)
		return self._si7

	@property
	def si8(self):
		"""si8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si8'):
			from .Si8 import Si8Cls
			self._si8 = Si8Cls(self._core, self._cmd_group)
		return self._si8

	@property
	def si9(self):
		"""si9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si9'):
			from .Si9 import Si9Cls
			self._si9 = Si9Cls(self._core, self._cmd_group)
		return self._si9

	@property
	def siInd(self):
		"""siInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_siInd'):
			from .SiInd import SiIndCls
			self._siInd = SiIndCls(self._core, self._cmd_group)
		return self._siInd

	@property
	def slIndex(self):
		"""slIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slIndex'):
			from .SlIndex import SlIndexCls
			self._slIndex = SlIndexCls(self._core, self._cmd_group)
		return self._slIndex

	@property
	def smind(self):
		"""smind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smind'):
			from .Smind import SmindCls
			self._smind = SmindCls(self._core, self._cmd_group)
		return self._smind

	@property
	def smsgs(self):
		"""smsgs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smsgs'):
			from .Smsgs import SmsgsCls
			self._smsgs = SmsgsCls(self._core, self._cmd_group)
		return self._smsgs

	@property
	def soin(self):
		"""soin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soin'):
			from .Soin import SoinCls
			self._soin = SoinCls(self._core, self._cmd_group)
		return self._soin

	@property
	def spsConf(self):
		"""spsConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spsConf'):
			from .SpsConf import SpsConfCls
			self._spsConf = SpsConfCls(self._core, self._cmd_group)
		return self._spsConf

	@property
	def sr1(self):
		"""sr1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr1'):
			from .Sr1 import Sr1Cls
			self._sr1 = Sr1Cls(self._core, self._cmd_group)
		return self._sr1

	@property
	def sr10(self):
		"""sr10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr10'):
			from .Sr10 import Sr10Cls
			self._sr10 = Sr10Cls(self._core, self._cmd_group)
		return self._sr10

	@property
	def sr11(self):
		"""sr11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr11'):
			from .Sr11 import Sr11Cls
			self._sr11 = Sr11Cls(self._core, self._cmd_group)
		return self._sr11

	@property
	def sr2(self):
		"""sr2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr2'):
			from .Sr2 import Sr2Cls
			self._sr2 = Sr2Cls(self._core, self._cmd_group)
		return self._sr2

	@property
	def sr3(self):
		"""sr3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr3'):
			from .Sr3 import Sr3Cls
			self._sr3 = Sr3Cls(self._core, self._cmd_group)
		return self._sr3

	@property
	def sr4(self):
		"""sr4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr4'):
			from .Sr4 import Sr4Cls
			self._sr4 = Sr4Cls(self._core, self._cmd_group)
		return self._sr4

	@property
	def sr5(self):
		"""sr5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr5'):
			from .Sr5 import Sr5Cls
			self._sr5 = Sr5Cls(self._core, self._cmd_group)
		return self._sr5

	@property
	def sr6(self):
		"""sr6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr6'):
			from .Sr6 import Sr6Cls
			self._sr6 = Sr6Cls(self._core, self._cmd_group)
		return self._sr6

	@property
	def sr7(self):
		"""sr7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr7'):
			from .Sr7 import Sr7Cls
			self._sr7 = Sr7Cls(self._core, self._cmd_group)
		return self._sr7

	@property
	def sr8(self):
		"""sr8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr8'):
			from .Sr8 import Sr8Cls
			self._sr8 = Sr8Cls(self._core, self._cmd_group)
		return self._sr8

	@property
	def sr9(self):
		"""sr9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr9'):
			from .Sr9 import Sr9Cls
			self._sr9 = Sr9Cls(self._core, self._cmd_group)
		return self._sr9

	@property
	def sri2(self):
		"""sri2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sri2'):
			from .Sri2 import Sri2Cls
			self._sri2 = Sri2Cls(self._core, self._cmd_group)
		return self._sri2

	@property
	def srInd(self):
		"""srInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srInd'):
			from .SrInd import SrIndCls
			self._srInd = SrIndCls(self._core, self._cmd_group)
		return self._srInd

	@property
	def srsRequest(self):
		"""srsRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsRequest'):
			from .SrsRequest import SrsRequestCls
			self._srsRequest = SrsRequestCls(self._core, self._cmd_group)
		return self._srsRequest

	@property
	def srsResInd(self):
		"""srsResInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsResInd'):
			from .SrsResInd import SrsResIndCls
			self._srsResInd = SrsResIndCls(self._core, self._cmd_group)
		return self._srsResInd

	@property
	def ssp(self):
		"""ssp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssp'):
			from .Ssp import SspCls
			self._ssp = SspCls(self._core, self._cmd_group)
		return self._ssp

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def t2Pc(self):
		"""t2Pc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t2Pc'):
			from .T2Pc import T2PcCls
			self._t2Pc = T2PcCls(self._core, self._cmd_group)
		return self._t2Pc

	@property
	def t2Ps(self):
		"""t2Ps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t2Ps'):
			from .T2Ps import T2PsCls
			self._t2Ps = T2PsCls(self._core, self._cmd_group)
		return self._t2Ps

	@property
	def t3Cbind(self):
		"""t3Cbind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t3Cbind'):
			from .T3Cbind import T3CbindCls
			self._t3Cbind = T3CbindCls(self._core, self._cmd_group)
		return self._t3Cbind

	@property
	def tb1(self):
		"""tb1 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb1'):
			from .Tb1 import Tb1Cls
			self._tb1 = Tb1Cls(self._core, self._cmd_group)
		return self._tb1

	@property
	def tb2(self):
		"""tb2 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb2'):
			from .Tb2 import Tb2Cls
			self._tb2 = Tb2Cls(self._core, self._cmd_group)
		return self._tb2

	@property
	def tbScaling(self):
		"""tbScaling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbScaling'):
			from .TbScaling import TbScalingCls
			self._tbScaling = TbScalingCls(self._core, self._cmd_group)
		return self._tbScaling

	@property
	def tci(self):
		"""tci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tci'):
			from .Tci import TciCls
			self._tci = TciCls(self._core, self._cmd_group)
		return self._tci

	@property
	def tgap(self):
		"""tgap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tgap'):
			from .Tgap import TgapCls
			self._tgap = TgapCls(self._core, self._cmd_group)
		return self._tgap

	@property
	def tidRes(self):
		"""tidRes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tidRes'):
			from .TidRes import TidResCls
			self._tidRes = TidResCls(self._core, self._cmd_group)
		return self._tidRes

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Toffset import ToffsetCls
			self._toffset = ToffsetCls(self._core, self._cmd_group)
		return self._toffset

	@property
	def tp1(self):
		"""tp1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp1'):
			from .Tp1 import Tp1Cls
			self._tp1 = Tp1Cls(self._core, self._cmd_group)
		return self._tp1

	@property
	def tp10(self):
		"""tp10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp10'):
			from .Tp10 import Tp10Cls
			self._tp10 = Tp10Cls(self._core, self._cmd_group)
		return self._tp10

	@property
	def tp11(self):
		"""tp11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp11'):
			from .Tp11 import Tp11Cls
			self._tp11 = Tp11Cls(self._core, self._cmd_group)
		return self._tp11

	@property
	def tp12(self):
		"""tp12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp12'):
			from .Tp12 import Tp12Cls
			self._tp12 = Tp12Cls(self._core, self._cmd_group)
		return self._tp12

	@property
	def tp13(self):
		"""tp13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp13'):
			from .Tp13 import Tp13Cls
			self._tp13 = Tp13Cls(self._core, self._cmd_group)
		return self._tp13

	@property
	def tp14(self):
		"""tp14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp14'):
			from .Tp14 import Tp14Cls
			self._tp14 = Tp14Cls(self._core, self._cmd_group)
		return self._tp14

	@property
	def tp15(self):
		"""tp15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp15'):
			from .Tp15 import Tp15Cls
			self._tp15 = Tp15Cls(self._core, self._cmd_group)
		return self._tp15

	@property
	def tp16(self):
		"""tp16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp16'):
			from .Tp16 import Tp16Cls
			self._tp16 = Tp16Cls(self._core, self._cmd_group)
		return self._tp16

	@property
	def tp17(self):
		"""tp17 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp17'):
			from .Tp17 import Tp17Cls
			self._tp17 = Tp17Cls(self._core, self._cmd_group)
		return self._tp17

	@property
	def tp18(self):
		"""tp18 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp18'):
			from .Tp18 import Tp18Cls
			self._tp18 = Tp18Cls(self._core, self._cmd_group)
		return self._tp18

	@property
	def tp19(self):
		"""tp19 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp19'):
			from .Tp19 import Tp19Cls
			self._tp19 = Tp19Cls(self._core, self._cmd_group)
		return self._tp19

	@property
	def tp2(self):
		"""tp2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp2'):
			from .Tp2 import Tp2Cls
			self._tp2 = Tp2Cls(self._core, self._cmd_group)
		return self._tp2

	@property
	def tp20(self):
		"""tp20 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp20'):
			from .Tp20 import Tp20Cls
			self._tp20 = Tp20Cls(self._core, self._cmd_group)
		return self._tp20

	@property
	def tp21(self):
		"""tp21 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp21'):
			from .Tp21 import Tp21Cls
			self._tp21 = Tp21Cls(self._core, self._cmd_group)
		return self._tp21

	@property
	def tp22(self):
		"""tp22 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp22'):
			from .Tp22 import Tp22Cls
			self._tp22 = Tp22Cls(self._core, self._cmd_group)
		return self._tp22

	@property
	def tp3(self):
		"""tp3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp3'):
			from .Tp3 import Tp3Cls
			self._tp3 = Tp3Cls(self._core, self._cmd_group)
		return self._tp3

	@property
	def tp4(self):
		"""tp4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp4'):
			from .Tp4 import Tp4Cls
			self._tp4 = Tp4Cls(self._core, self._cmd_group)
		return self._tp4

	@property
	def tp5(self):
		"""tp5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp5'):
			from .Tp5 import Tp5Cls
			self._tp5 = Tp5Cls(self._core, self._cmd_group)
		return self._tp5

	@property
	def tp6(self):
		"""tp6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp6'):
			from .Tp6 import Tp6Cls
			self._tp6 = Tp6Cls(self._core, self._cmd_group)
		return self._tp6

	@property
	def tp7(self):
		"""tp7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp7'):
			from .Tp7 import Tp7Cls
			self._tp7 = Tp7Cls(self._core, self._cmd_group)
		return self._tp7

	@property
	def tp8(self):
		"""tp8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp8'):
			from .Tp8 import Tp8Cls
			self._tp8 = Tp8Cls(self._core, self._cmd_group)
		return self._tp8

	@property
	def tp9(self):
		"""tp9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp9'):
			from .Tp9 import Tp9Cls
			self._tp9 = Tp9Cls(self._core, self._cmd_group)
		return self._tp9

	@property
	def tpucch(self):
		"""tpucch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpucch'):
			from .Tpucch import TpucchCls
			self._tpucch = TpucchCls(self._core, self._cmd_group)
		return self._tpucch

	@property
	def tpusch(self):
		"""tpusch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpusch'):
			from .Tpusch import TpuschCls
			self._tpusch = TpuschCls(self._core, self._cmd_group)
		return self._tpusch

	@property
	def trav(self):
		"""trav commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trav'):
			from .Trav import TravCls
			self._trav = TravCls(self._core, self._cmd_group)
		return self._trav

	@property
	def ulSchInd(self):
		"""ulSchInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulSchInd'):
			from .UlSchInd import UlSchIndCls
			self._ulSchInd = UlSchIndCls(self._core, self._cmd_group)
		return self._ulSchInd

	@property
	def usage(self):
		"""usage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usage'):
			from .Usage import UsageCls
			self._usage = UsageCls(self._core, self._cmd_group)
		return self._usage

	@property
	def usInd(self):
		"""usInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usInd'):
			from .UsInd import UsIndCls
			self._usInd = UsIndCls(self._core, self._cmd_group)
		return self._usInd

	@property
	def vtprb(self):
		"""vtprb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vtprb'):
			from .Vtprb import VtprbCls
			self._vtprb = VtprbCls(self._core, self._cmd_group)
		return self._vtprb

	@property
	def wa1(self):
		"""wa1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa1'):
			from .Wa1 import Wa1Cls
			self._wa1 = Wa1Cls(self._core, self._cmd_group)
		return self._wa1

	@property
	def wa10(self):
		"""wa10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa10'):
			from .Wa10 import Wa10Cls
			self._wa10 = Wa10Cls(self._core, self._cmd_group)
		return self._wa10

	@property
	def wa2(self):
		"""wa2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa2'):
			from .Wa2 import Wa2Cls
			self._wa2 = Wa2Cls(self._core, self._cmd_group)
		return self._wa2

	@property
	def wa3(self):
		"""wa3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa3'):
			from .Wa3 import Wa3Cls
			self._wa3 = Wa3Cls(self._core, self._cmd_group)
		return self._wa3

	@property
	def wa4(self):
		"""wa4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa4'):
			from .Wa4 import Wa4Cls
			self._wa4 = Wa4Cls(self._core, self._cmd_group)
		return self._wa4

	@property
	def wa5(self):
		"""wa5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa5'):
			from .Wa5 import Wa5Cls
			self._wa5 = Wa5Cls(self._core, self._cmd_group)
		return self._wa5

	@property
	def wa6(self):
		"""wa6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa6'):
			from .Wa6 import Wa6Cls
			self._wa6 = Wa6Cls(self._core, self._cmd_group)
		return self._wa6

	@property
	def wa7(self):
		"""wa7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa7'):
			from .Wa7 import Wa7Cls
			self._wa7 = Wa7Cls(self._core, self._cmd_group)
		return self._wa7

	@property
	def wa8(self):
		"""wa8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa8'):
			from .Wa8 import Wa8Cls
			self._wa8 = Wa8Cls(self._core, self._cmd_group)
		return self._wa8

	@property
	def wa9(self):
		"""wa9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa9'):
			from .Wa9 import Wa9Cls
			self._wa9 = Wa9Cls(self._core, self._cmd_group)
		return self._wa9

	@property
	def zcrTrigg(self):
		"""zcrTrigg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zcrTrigg'):
			from .ZcrTrigg import ZcrTriggCls
			self._zcrTrigg = ZcrTriggCls(self._core, self._cmd_group)
		return self._zcrTrigg

	def clone(self) -> 'DciCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DciCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
