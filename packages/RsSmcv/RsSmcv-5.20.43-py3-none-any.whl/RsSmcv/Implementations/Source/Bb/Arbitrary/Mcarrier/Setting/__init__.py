from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 4 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_store'):
			from .Store import StoreCls
			self._store = StoreCls(self._core, self._cmd_group)
		return self._store

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.bb.arbitrary.mcarrier.setting.get_catalog() \n
		Queries the available settings files in the specified default directory. Only files with the file extension *.
		arb_multcarr are listed. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:MCARrier:SETTing:LOAD \n
		Snippet: driver.source.bb.arbitrary.mcarrier.setting.load(filename = 'abc') \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.arb_multcarr.
		Refer to 'Accessing files in the default or in a specified directory' for general information on file handling in the
		default and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:SETTing:LOAD {param}')

	def clone(self) -> 'SettingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SettingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
