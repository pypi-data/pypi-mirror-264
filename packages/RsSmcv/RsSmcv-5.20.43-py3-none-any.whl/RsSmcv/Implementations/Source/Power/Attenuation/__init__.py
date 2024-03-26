from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AttenuationCls:
	"""Attenuation commands group definition. 4 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuation", core, parent)

	@property
	def rfOff(self):
		"""rfOff commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfOff'):
			from .RfOff import RfOffCls
			self._rfOff = RfOffCls(self._core, self._cmd_group)
		return self._rfOff

	@property
	def sover(self):
		"""sover commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sover'):
			from .Sover import SoverCls
			self._sover = SoverCls(self._core, self._cmd_group)
		return self._sover

	def get_digital(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:DIGital \n
		Snippet: value: float = driver.source.power.attenuation.get_digital() \n
		No command help available \n
			:return: att_digital: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:DIGital?')
		return Conversions.str_to_float(response)

	def set_digital(self, att_digital: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:DIGital \n
		Snippet: driver.source.power.attenuation.set_digital(att_digital = 1.0) \n
		No command help available \n
			:param att_digital: No help available
		"""
		param = Conversions.decimal_value_to_str(att_digital)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ATTenuation:DIGital {param}')

	def get_stage(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:ATTenuation:STAGe \n
		Snippet: value: float = driver.source.power.attenuation.get_stage() \n
		No command help available \n
			:return: stage: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:STAGe?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'AttenuationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AttenuationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
