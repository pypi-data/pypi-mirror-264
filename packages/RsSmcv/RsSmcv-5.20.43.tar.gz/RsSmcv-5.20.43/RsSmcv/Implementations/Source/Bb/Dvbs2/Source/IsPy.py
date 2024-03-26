from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IsPyCls:
	"""IsPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("isPy", core, parent)

	# noinspection PyTypeChecker
	def get(self, inputStream=repcap.InputStream.Nr1) -> enums.CodingInputSignalSource:
		"""SCPI: [SOURce<HW>]:BB:DVBS2:SOURce:IS<CH> \n
		Snippet: value: enums.CodingInputSignalSource = driver.source.bb.dvbs2.source.isPy.get(inputStream = repcap.InputStream.Nr1) \n
		For VCM mode, queries the source for input streams 2 to 8. This source is always a test signal. \n
			:param inputStream: optional repeated capability selector. Default value: Nr1
			:return: source: TESTsignal"""
		inputStream_cmd_val = self._cmd_group.get_repcap_cmd_value(inputStream, repcap.InputStream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DVBS2:SOURce:IS{inputStream_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.CodingInputSignalSource)
