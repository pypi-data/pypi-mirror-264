from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MagnitudeCls:
	"""Magnitude commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("magnitude", core, parent)

	def set(self, ipartq_ratio: float, iqConnector=repcap.IqConnector.Default) -> None:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:IQRatio:[MAGNitude] \n
		Snippet: driver.source.bb.impairment.iqOutput.iqRatio.magnitude.set(ipartq_ratio = 1.0, iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param ipartq_ratio: No help available
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
		"""
		param = Conversions.decimal_value_to_str(ipartq_ratio)
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		self._core.io.write(f'SOURce:BB:IMPairment:IQOutput{iqConnector_cmd_val}:IQRatio:MAGNitude {param}')

	def get(self, iqConnector=repcap.IqConnector.Default) -> float:
		"""SCPI: [SOURce]:BB:IMPairment:IQOutput<CH>:IQRatio:[MAGNitude] \n
		Snippet: value: float = driver.source.bb.impairment.iqOutput.iqRatio.magnitude.get(iqConnector = repcap.IqConnector.Default) \n
		No command help available \n
			:param iqConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: ipartq_ratio: No help available"""
		iqConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(iqConnector, repcap.IqConnector)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:IQOutput{iqConnector_cmd_val}:IQRatio:MAGNitude?')
		return Conversions.str_to_float(response)
