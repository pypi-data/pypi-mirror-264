from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PciExpressCls:
	"""PciExpress commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pciExpress", core, parent)

	def get_resource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:PCIexpress:RESource \n
		Snippet: value: str = driver.system.communicate.pciExpress.get_resource() \n
		No command help available \n
			:return: resource: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:PCIexpress:RESource?')
		return trim_str_response(response)
