from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoteCls:
	"""Remote commands group definition. 11 total commands, 7 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("remote", core, parent)

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .Add import AddCls
			self._add = AddCls(self._core, self._cmd_group)
		return self._add

	@property
	def clean(self):
		"""clean commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_clean'):
			from .Clean import CleanCls
			self._clean = CleanCls(self._core, self._cmd_group)
		return self._clean

	@property
	def connect(self):
		"""connect commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_connect'):
			from .Connect import ConnectCls
			self._connect = ConnectCls(self._core, self._cmd_group)
		return self._connect

	@property
	def disconnect(self):
		"""disconnect commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_disconnect'):
			from .Disconnect import DisconnectCls
			self._disconnect = DisconnectCls(self._core, self._cmd_group)
		return self._disconnect

	@property
	def initialization(self):
		"""initialization commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_initialization'):
			from .Initialization import InitializationCls
			self._initialization = InitializationCls(self._core, self._cmd_group)
		return self._initialization

	@property
	def purge(self):
		"""purge commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_purge'):
			from .Purge import PurgeCls
			self._purge = PurgeCls(self._core, self._cmd_group)
		return self._purge

	@property
	def scan(self):
		"""scan commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_scan'):
			from .Scan import ScanCls
			self._scan = ScanCls(self._core, self._cmd_group)
		return self._scan

	def delete(self, id_pi_db_ext_dev_rem_inst_remove: List[str]) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:DELete \n
		Snippet: driver.sconfiguration.external.remote.delete(id_pi_db_ext_dev_rem_inst_remove = ['abc1', 'abc2', 'abc3']) \n
		No command help available \n
			:param id_pi_db_ext_dev_rem_inst_remove: No help available
		"""
		param = Conversions.list_to_csv_quoted_str(id_pi_db_ext_dev_rem_inst_remove)
		self._core.io.write(f'SCONfiguration:EXTernal:REMote:DELete {param}')

	def get_list_py(self) -> List[str]:
		"""SCPI: SCONfiguration:EXTernal:REMote:LIST \n
		Snippet: value: List[str] = driver.sconfiguration.external.remote.get_list_py() \n
		Lists all available instruments. Instruments found, e.g. by the method RsSmbv.Sconfiguration.External.Remote.Scan.
		set command. \n
			:return: instr_names: String String with symbolic names and/or alias names
		"""
		response = self._core.io.query_str('SCONfiguration:EXTernal:REMote:LIST?')
		return Conversions.str_to_str_list(response)

	def set_rename(self, id_pi_db_rem_inst_rename: List[str]) -> None:
		"""SCPI: SCONfiguration:EXTernal:REMote:REName \n
		Snippet: driver.sconfiguration.external.remote.set_rename(id_pi_db_rem_inst_rename = ['abc1', 'abc2', 'abc3']) \n
		Changes the symbolic name of the instrument. \n
			:param id_pi_db_rem_inst_rename: No help available
		"""
		param = Conversions.list_to_csv_quoted_str(id_pi_db_rem_inst_rename)
		self._core.io.write(f'SCONfiguration:EXTernal:REMote:REName {param}')

	def clone(self) -> 'RemoteCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RemoteCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
