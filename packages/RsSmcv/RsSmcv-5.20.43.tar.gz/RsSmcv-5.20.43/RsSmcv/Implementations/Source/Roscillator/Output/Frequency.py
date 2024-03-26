from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.RoscOutpFreqMode:
		"""SCPI: [SOURce]:ROSCillator:OUTPut:FREQuency:MODE \n
		Snippet: value: enums.RoscOutpFreqMode = driver.source.roscillator.output.frequency.get_mode() \n
		Selects the mode for the output reference frequency. \n
			:return: outp_freq_mode: DER10M| OFF| LOOPthrough OFF Disables the output. DER10M Sets the output reference frequency to 10 MHz. The reference frequency is derived from the internal reference frequency. LOOPthrough Forwards the input reference frequency to the reference frequency output.
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:OUTPut:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.RoscOutpFreqMode)

	def set_mode(self, outp_freq_mode: enums.RoscOutpFreqMode) -> None:
		"""SCPI: [SOURce]:ROSCillator:OUTPut:FREQuency:MODE \n
		Snippet: driver.source.roscillator.output.frequency.set_mode(outp_freq_mode = enums.RoscOutpFreqMode.DER10M) \n
		Selects the mode for the output reference frequency. \n
			:param outp_freq_mode: DER10M| OFF| LOOPthrough OFF Disables the output. DER10M Sets the output reference frequency to 10 MHz. The reference frequency is derived from the internal reference frequency. LOOPthrough Forwards the input reference frequency to the reference frequency output.
		"""
		param = Conversions.enum_scalar_to_str(outp_freq_mode, enums.RoscOutpFreqMode)
		self._core.io.write(f'SOURce:ROSCillator:OUTPut:FREQuency:MODE {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.EmulSgtRoscOutputFreq:
		"""SCPI: [SOURce<HW>]:ROSCillator:OUTPut:FREQuency \n
		Snippet: value: enums.EmulSgtRoscOutputFreq = driver.source.roscillator.output.frequency.get_value() \n
		No command help available \n
			:return: output_freq: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ROSCillator:OUTPut:FREQuency?')
		return Conversions.str_to_scalar_enum(response, enums.EmulSgtRoscOutputFreq)

	def set_value(self, output_freq: enums.EmulSgtRoscOutputFreq) -> None:
		"""SCPI: [SOURce<HW>]:ROSCillator:OUTPut:FREQuency \n
		Snippet: driver.source.roscillator.output.frequency.set_value(output_freq = enums.EmulSgtRoscOutputFreq._1000MHZ) \n
		No command help available \n
			:param output_freq: No help available
		"""
		param = Conversions.enum_scalar_to_str(output_freq, enums.EmulSgtRoscOutputFreq)
		self._core.io.write(f'SOURce<HwInstance>:ROSCillator:OUTPut:FREQuency {param}')
