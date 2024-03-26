from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnvelopeCls:
	"""Envelope commands group definition. 47 total commands, 7 Subgroups, 12 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("envelope", core, parent)

	@property
	def emf(self):
		"""emf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_emf'):
			from .Emf import EmfCls
			self._emf = EmfCls(self._core, self._cmd_group)
		return self._emf

	@property
	def pin(self):
		"""pin commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pin'):
			from .Pin import PinCls
			self._pin = PinCls(self._core, self._cmd_group)
		return self._pin

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def shaping(self):
		"""shaping commands group. 6 Sub-classes, 3 commands."""
		if not hasattr(self, '_shaping'):
			from .Shaping import ShapingCls
			self._shaping = ShapingCls(self._core, self._cmd_group)
		return self._shaping

	@property
	def vcc(self):
		"""vcc commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_vcc'):
			from .Vcc import VccCls
			self._vcc = VccCls(self._core, self._cmd_group)
		return self._vcc

	@property
	def vout(self):
		"""vout commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_vout'):
			from .Vout import VoutCls
			self._vout = VoutCls(self._core, self._cmd_group)
		return self._vout

	@property
	def vpp(self):
		"""vpp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vpp'):
			from .Vpp import VppCls
			self._vpp = VppCls(self._core, self._cmd_group)
		return self._vpp

	# noinspection PyTypeChecker
	def get_adaption(self) -> enums.IqOutEnvAdaption:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ADAPtion \n
		Snippet: value: enums.IqOutEnvAdaption = driver.source.iq.output.analog.envelope.get_adaption() \n
		No command help available \n
			:return: adaption_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ADAPtion?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvAdaption)

	def set_adaption(self, adaption_mode: enums.IqOutEnvAdaption) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ADAPtion \n
		Snippet: driver.source.iq.output.analog.envelope.set_adaption(adaption_mode = enums.IqOutEnvAdaption.AUTO) \n
		No command help available \n
			:param adaption_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(adaption_mode, enums.IqOutEnvAdaption)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ADAPtion {param}')

	def get_bias(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BIAS \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_bias() \n
		No command help available \n
			:return: bias: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BIAS?')
		return Conversions.str_to_float(response)

	def set_bias(self, bias: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BIAS \n
		Snippet: driver.source.iq.output.analog.envelope.set_bias(bias = 1.0) \n
		No command help available \n
			:param bias: No help available
		"""
		param = Conversions.decimal_value_to_str(bias)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BIAS {param}')

	def get_binput(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BINPut \n
		Snippet: value: bool = driver.source.iq.output.analog.envelope.get_binput() \n
		No command help available \n
			:return: bipolar_input: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BINPut?')
		return Conversions.str_to_bool(response)

	def set_binput(self, bipolar_input: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:BINPut \n
		Snippet: driver.source.iq.output.analog.envelope.set_binput(bipolar_input = False) \n
		No command help available \n
			:param bipolar_input: No help available
		"""
		param = Conversions.bool_to_str(bipolar_input)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:BINPut {param}')

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:DELay \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:DELay \n
		Snippet: driver.source.iq.output.analog.envelope.set_delay(delay = 1.0) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:DELay {param}')

	# noinspection PyTypeChecker
	def get_etrak(self) -> enums.IqOutEnvEtRak:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ETRak \n
		Snippet: value: enums.IqOutEnvEtRak = driver.source.iq.output.analog.envelope.get_etrak() \n
		No command help available \n
			:return: etrak_ifc_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ETRak?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvEtRak)

	def set_etrak(self, etrak_ifc_type: enums.IqOutEnvEtRak) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:ETRak \n
		Snippet: driver.source.iq.output.analog.envelope.set_etrak(etrak_ifc_type = enums.IqOutEnvEtRak.ET1V2) \n
		No command help available \n
			:param etrak_ifc_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(etrak_ifc_type, enums.IqOutEnvEtRak)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:ETRak {param}')

	def get_fdpd(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:FDPD \n
		Snippet: value: bool = driver.source.iq.output.analog.envelope.get_fdpd() \n
		No command help available \n
			:return: calc_from_dpd_stat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:FDPD?')
		return Conversions.str_to_bool(response)

	def set_fdpd(self, calc_from_dpd_stat: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:FDPD \n
		Snippet: driver.source.iq.output.analog.envelope.set_fdpd(calc_from_dpd_stat = False) \n
		No command help available \n
			:param calc_from_dpd_stat: No help available
		"""
		param = Conversions.bool_to_str(calc_from_dpd_stat)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:FDPD {param}')

	def get_gain(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:GAIN \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_gain() \n
		No command help available \n
			:return: gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:GAIN?')
		return Conversions.str_to_float(response)

	def set_gain(self, gain: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:GAIN \n
		Snippet: driver.source.iq.output.analog.envelope.set_gain(gain = 1.0) \n
		No command help available \n
			:param gain: No help available
		"""
		param = Conversions.decimal_value_to_str(gain)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:GAIN {param}')

	def get_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:OFFSet \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_offset() \n
		No command help available \n
			:return: offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:OFFSet \n
		Snippet: driver.source.iq.output.analog.envelope.set_offset(offset = 1.0) \n
		No command help available \n
			:param offset: No help available
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:OFFSet {param}')

	def get_rin(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:RIN \n
		Snippet: value: float = driver.source.iq.output.analog.envelope.get_rin() \n
		No command help available \n
			:return: ipart_nput_resistance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:RIN?')
		return Conversions.str_to_float(response)

	def set_rin(self, ipart_nput_resistance: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:RIN \n
		Snippet: driver.source.iq.output.analog.envelope.set_rin(ipart_nput_resistance = 1.0) \n
		No command help available \n
			:param ipart_nput_resistance: No help available
		"""
		param = Conversions.decimal_value_to_str(ipart_nput_resistance)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:RIN {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:STATe \n
		Snippet: value: bool = driver.source.iq.output.analog.envelope.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:STATe \n
		Snippet: driver.source.iq.output.analog.envelope.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:STATe {param}')

	# noinspection PyTypeChecker
	def get_termination(self) -> enums.IqOutEnvTerm:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:TERMination \n
		Snippet: value: enums.IqOutEnvTerm = driver.source.iq.output.analog.envelope.get_termination() \n
		No command help available \n
			:return: termination: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:TERMination?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvTerm)

	def set_termination(self, termination: enums.IqOutEnvTerm) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:TERMination \n
		Snippet: driver.source.iq.output.analog.envelope.set_termination(termination = enums.IqOutEnvTerm.GROund) \n
		No command help available \n
			:param termination: No help available
		"""
		param = Conversions.enum_scalar_to_str(termination, enums.IqOutEnvTerm)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:TERMination {param}')

	# noinspection PyTypeChecker
	def get_vref(self) -> enums.IqOutEnvVrEf:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VREF \n
		Snippet: value: enums.IqOutEnvVrEf = driver.source.iq.output.analog.envelope.get_vref() \n
		No command help available \n
			:return: voltage_reference: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VREF?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvVrEf)

	def set_vref(self, voltage_reference: enums.IqOutEnvVrEf) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VREF \n
		Snippet: driver.source.iq.output.analog.envelope.set_vref(voltage_reference = enums.IqOutEnvVrEf.VCC) \n
		No command help available \n
			:param voltage_reference: No help available
		"""
		param = Conversions.enum_scalar_to_str(voltage_reference, enums.IqOutEnvVrEf)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VREF {param}')

	def clone(self) -> 'EnvelopeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EnvelopeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
