from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SocketCls:
	"""Socket commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("socket", core, parent)

	def get_port(self) -> int:
		"""SCPI: SYSTem:COMMunicate:SOCKet:PORT \n
		Snippet: value: int = driver.system.communicate.socket.get_port() \n
		No command help available \n
			:return: scpi_eth_port: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, scpi_eth_port: int) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:PORT \n
		Snippet: driver.system.communicate.socket.set_port(scpi_eth_port = 1) \n
		No command help available \n
			:param scpi_eth_port: No help available
		"""
		param = Conversions.decimal_value_to_str(scpi_eth_port)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:PORT {param}')

	def get_resource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SOCKet:RESource \n
		Snippet: value: str = driver.system.communicate.socket.get_resource() \n
		Queries the visa resource string for remote control via LAN interface, using TCP/IP socket protocol. \n
			:return: resource: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:RESource?')
		return trim_str_response(response)
