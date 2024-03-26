from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SingleCls:
	"""Single commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("single", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:SINGle \n
		Snippet: driver.source.power.spc.single.set() \n
		Triggers the power sensor to measure the power value once. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:POWer:SPC:SINGle')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SPC:SINGle \n
		Snippet: driver.source.power.spc.single.set_with_opc() \n
		Triggers the power sensor to measure the power value once. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmcv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:POWer:SPC:SINGle', opc_timeout_ms)
