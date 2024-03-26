from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)

	def get_cfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DPD:INPut:CFACtor \n
		Snippet: value: float = driver.source.iq.dpd.inputPy.get_cfactor() \n
		No command help available \n
			:return: crest_factor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:INPut:CFACtor?')
		return Conversions.str_to_float(response)

	def get_level(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DPD:INPut:LEVel \n
		Snippet: value: float = driver.source.iq.dpd.inputPy.get_level() \n
		No command help available \n
			:return: level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:INPut:LEVel?')
		return Conversions.str_to_float(response)

	def get_pep(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:DPD:INPut:PEP \n
		Snippet: value: float = driver.source.iq.dpd.inputPy.get_pep() \n
		No command help available \n
			:return: pep: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:INPut:PEP?')
		return Conversions.str_to_float(response)
