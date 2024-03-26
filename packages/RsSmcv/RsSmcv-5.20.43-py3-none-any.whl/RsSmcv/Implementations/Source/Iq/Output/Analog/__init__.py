from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnalogCls:
	"""Analog commands group definition. 59 total commands, 4 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("analog", core, parent)

	@property
	def bias(self):
		"""bias commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_bias'):
			from .Bias import BiasCls
			self._bias = BiasCls(self._core, self._cmd_group)
		return self._bias

	@property
	def envelope(self):
		"""envelope commands group. 7 Sub-classes, 12 commands."""
		if not hasattr(self, '_envelope'):
			from .Envelope import EnvelopeCls
			self._envelope = EnvelopeCls(self._core, self._cmd_group)
		return self._envelope

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.IqOutMode:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Snippet: value: enums.IqOutMode = driver.source.iq.output.analog.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutMode)

	def set_mode(self, mode: enums.IqOutMode) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Snippet: driver.source.iq.output.analog.set_mode(mode = enums.IqOutMode.FIXed) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.IqOutMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Snippet: driver.source.iq.output.analog.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Snippet: driver.source.iq.output.analog.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmcv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.IqOutType:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Snippet: value: enums.IqOutType = driver.source.iq.output.analog.get_type_py() \n
		No command help available \n
			:return: type_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutType)

	def set_type_py(self, type_py: enums.IqOutType) -> None:
		"""SCPI: [SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Snippet: driver.source.iq.output.analog.set_type_py(type_py = enums.IqOutType.DIFFerential) \n
		No command help available \n
			:param type_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.IqOutType)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE {param}')

	def clone(self) -> 'AnalogCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AnalogCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
