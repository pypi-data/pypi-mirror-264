from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RefLoCls:
	"""RefLo commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("refLo", core, parent)

	# noinspection PyTypeChecker
	def get_output(self) -> enums.EmulSgtRefLoOutput:
		"""SCPI: CONNector:REFLo:OUTPut \n
		Snippet: value: enums.EmulSgtRefLoOutput = driver.connector.refLo.get_output() \n
		No command help available \n
			:return: output: No help available
		"""
		response = self._core.io.query_str('CONNector:REFLo:OUTPut?')
		return Conversions.str_to_scalar_enum(response, enums.EmulSgtRefLoOutput)

	def set_output(self, output: enums.EmulSgtRefLoOutput) -> None:
		"""SCPI: CONNector:REFLo:OUTPut \n
		Snippet: driver.connector.refLo.set_output(output = enums.EmulSgtRefLoOutput.LO) \n
		No command help available \n
			:param output: No help available
		"""
		param = Conversions.enum_scalar_to_str(output, enums.EmulSgtRefLoOutput)
		self._core.io.write(f'CONNector:REFLo:OUTPut {param}')
