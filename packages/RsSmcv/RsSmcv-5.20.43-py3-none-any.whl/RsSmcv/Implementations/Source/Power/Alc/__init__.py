from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlcCls:
	"""Alc commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alc", core, parent)

	@property
	def sonce(self):
		"""sonce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sonce'):
			from .Sonce import SonceCls
			self._sonce = SonceCls(self._core, self._cmd_group)
		return self._sonce

	# noinspection PyTypeChecker
	def get_dsensitivity(self) -> enums.PowAlcDetSensitivityEmulSgt:
		"""SCPI: [SOURce<HW>]:POWer:ALC:DSENsitivity \n
		Snippet: value: enums.PowAlcDetSensitivityEmulSgt = driver.source.power.alc.get_dsensitivity() \n
		No command help available \n
			:return: sensitivity: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:DSENsitivity?')
		return Conversions.str_to_scalar_enum(response, enums.PowAlcDetSensitivityEmulSgt)

	def set_dsensitivity(self, sensitivity: enums.PowAlcDetSensitivityEmulSgt) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:DSENsitivity \n
		Snippet: driver.source.power.alc.set_dsensitivity(sensitivity = enums.PowAlcDetSensitivityEmulSgt.AUTO) \n
		No command help available \n
			:param sensitivity: No help available
		"""
		param = Conversions.enum_scalar_to_str(sensitivity, enums.PowAlcDetSensitivityEmulSgt)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:DSENsitivity {param}')

	# noinspection PyTypeChecker
	def get_state(self) -> enums.PowAlcStateEmulSgt:
		"""SCPI: [SOURce<HW>]:POWer:ALC:[STATe] \n
		Snippet: value: enums.PowAlcStateEmulSgt = driver.source.power.alc.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ALC:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.PowAlcStateEmulSgt)

	def set_state(self, state: enums.PowAlcStateEmulSgt) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ALC:[STATe] \n
		Snippet: driver.source.power.alc.set_state(state = enums.PowAlcStateEmulSgt._0) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.enum_scalar_to_str(state, enums.PowAlcStateEmulSgt)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ALC:STATe {param}')

	def clone(self) -> 'AlcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AlcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
