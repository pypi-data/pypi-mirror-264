from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfWaveformCls:
	"""CfWaveform commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfWaveform", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CFR:CFWaveform:[STATe] \n
		Snippet: value: bool = driver.source.bb.arbitrary.cfr.cfWaveform.get_state() \n
		No command help available \n
			:return: arb_cfr_cfw_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CFR:CFWaveform:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, arb_cfr_cfw_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:CFR:CFWaveform:[STATe] \n
		Snippet: driver.source.bb.arbitrary.cfr.cfWaveform.set_state(arb_cfr_cfw_state = False) \n
		No command help available \n
			:param arb_cfr_cfw_state: No help available
		"""
		param = Conversions.bool_to_str(arb_cfr_cfw_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CFR:CFWaveform:STATe {param}')
