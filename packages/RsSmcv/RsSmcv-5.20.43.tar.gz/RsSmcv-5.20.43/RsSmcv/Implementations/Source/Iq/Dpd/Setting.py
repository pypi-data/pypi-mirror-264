from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SettingCls:
	"""Setting commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setting", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SETTing:CATalog \n
		Snippet: value: List[str] = driver.source.iq.dpd.setting.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SETTing:LOAD \n
		Snippet: driver.source.iq.dpd.setting.load(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:SETTing:STORe \n
		Snippet: driver.source.iq.dpd.setting.set_store(filename = 'abc') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:SETTing:STORe {param}')
