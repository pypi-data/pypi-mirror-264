from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VppCls:
	"""Vpp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vpp", core, parent)

	def get_max(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VPP:[MAX] \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.vpp.get_max() \n
		No command help available \n
			:return: vpp_max: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VPP:MAX?')
		return Conversions.str_to_float(response)

	def set_max(self, vpp_max: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VPP:[MAX] \n
		Snippet: driver.source.iq.output.analog.envelope.vpp.set_max(vpp_max = 1.0) \n
		No command help available \n
			:param vpp_max: No help available
		"""
		param = Conversions.decimal_value_to_str(vpp_max)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VPP:MAX {param}')
