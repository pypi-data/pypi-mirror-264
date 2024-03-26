from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DpdCls:
	"""Dpd commands group definition. 47 total commands, 9 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpd", core, parent)

	@property
	def amam(self):
		"""amam commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_amam'):
			from .Amam import AmamCls
			self._amam = AmamCls(self._core, self._cmd_group)
		return self._amam

	@property
	def amPm(self):
		"""amPm commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_amPm'):
			from .AmPm import AmPmCls
			self._amPm = AmPmCls(self._core, self._cmd_group)
		return self._amPm

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def inputPy(self):
		"""inputPy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def measurement(self):
		"""measurement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_measurement'):
			from .Measurement import MeasurementCls
			self._measurement = MeasurementCls(self._core, self._cmd_group)
		return self._measurement

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def pin(self):
		"""pin commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pin'):
			from .Pin import PinCls
			self._pin = PinCls(self._core, self._cmd_group)
		return self._pin

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def shaping(self):
		"""shaping commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_shaping'):
			from .Shaping import ShapingCls
			self._shaping = ShapingCls(self._core, self._cmd_group)
		return self._shaping

	def get_am_first(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:DPD:AMFirst \n
		Snippet: value: bool = driver.source.iq.dpd.get_am_first() \n
		No command help available \n
			:return: am_am_first_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:AMFirst?')
		return Conversions.str_to_bool(response)

	def set_am_first(self, am_am_first_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:AMFirst \n
		Snippet: driver.source.iq.dpd.set_am_first(am_am_first_state = False) \n
		No command help available \n
			:param am_am_first_state: No help available
		"""
		param = Conversions.bool_to_str(am_am_first_state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:AMFirst {param}')

	# noinspection PyTypeChecker
	def get_lreference(self) -> enums.DpdPowRef:
		"""SCPI: [SOURce<HW>]:IQ:DPD:LREFerence \n
		Snippet: value: enums.DpdPowRef = driver.source.iq.dpd.get_lreference() \n
		No command help available \n
			:return: level_reference: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:LREFerence?')
		return Conversions.str_to_scalar_enum(response, enums.DpdPowRef)

	def set_lreference(self, level_reference: enums.DpdPowRef) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:LREFerence \n
		Snippet: driver.source.iq.dpd.set_lreference(level_reference = enums.DpdPowRef.ADPD) \n
		No command help available \n
			:param level_reference: No help available
		"""
		param = Conversions.enum_scalar_to_str(level_reference, enums.DpdPowRef)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:LREFerence {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:PRESet \n
		Snippet: driver.source.iq.dpd.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:PRESet \n
		Snippet: driver.source.iq.dpd.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmcv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:IQ:DPD:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:DPD:STATe \n
		Snippet: value: bool = driver.source.iq.dpd.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DPD:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DPD:STATe \n
		Snippet: driver.source.iq.dpd.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD:STATe {param}')

	def clone(self) -> 'DpdCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DpdCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
