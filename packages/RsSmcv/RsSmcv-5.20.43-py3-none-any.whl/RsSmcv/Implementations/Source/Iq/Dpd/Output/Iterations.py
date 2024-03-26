from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IterationsCls:
	"""Iterations commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iterations", core, parent)

	def get_max(self) -> int:
		"""SCPI: [SOURce<HW>]:IQ:DPD:OUTPut:ITERations:MAX \n
		Snippet: value: int = driver.source.iq.dpd.output.iterations.get_max() \n
		No command help available \n
			:return: max_iterations: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:OUTPut:ITERations:MAX?')
		return Conversions.str_to_int(response)

	def set_max(self, max_iterations: int) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:OUTPut:ITERations:MAX \n
		Snippet: driver.source.iq.dpd.output.iterations.set_max(max_iterations = 1) \n
		No command help available \n
			:param max_iterations: No help available
		"""
		param = Conversions.decimal_value_to_str(max_iterations)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:OUTPut:ITERations:MAX {param}')
