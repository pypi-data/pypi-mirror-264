from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCls:
	"""Iq commands group definition. 140 total commands, 4 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iq", core, parent)

	@property
	def dpd(self):
		"""dpd commands group. 9 Sub-classes, 4 commands."""
		if not hasattr(self, '_dpd'):
			from .Dpd import DpdCls
			self._dpd = DpdCls(self._core, self._cmd_group)
		return self._dpd

	@property
	def impairment(self):
		"""impairment commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_impairment'):
			from .Impairment import ImpairmentCls
			self._impairment = ImpairmentCls(self._core, self._cmd_group)
		return self._impairment

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def swap(self):
		"""swap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swap'):
			from .Swap import SwapCls
			self._swap = SwapCls(self._core, self._cmd_group)
		return self._swap

	def get_crest_factor(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:CREStfactor \n
		Snippet: value: float = driver.source.iq.get_crest_factor() \n
		No command help available \n
			:return: crest_factor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:CREStfactor?')
		return Conversions.str_to_float(response)

	def set_crest_factor(self, crest_factor: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:CREStfactor \n
		Snippet: driver.source.iq.set_crest_factor(crest_factor = 1.0) \n
		No command help available \n
			:param crest_factor: No help available
		"""
		param = Conversions.decimal_value_to_str(crest_factor)
		self._core.io.write(f'SOURce<HwInstance>:IQ:CREStfactor {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.IqMode:
		"""SCPI: [SOURce<HW>]:IQ:SOURce \n
		Snippet: value: enums.IqMode = driver.source.iq.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.IqMode)

	def set_source(self, source: enums.IqMode) -> None:
		"""SCPI: [SOURce<HW>]:IQ:SOURce \n
		Snippet: driver.source.iq.set_source(source = enums.IqMode.ANALog) \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.IqMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:STATe \n
		Snippet: value: bool = driver.source.iq.get_state() \n
		Enables/disables the I/Q modulation. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:STATe \n
		Snippet: driver.source.iq.set_state(state = False) \n
		Enables/disables the I/Q modulation. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:STATe {param}')

	def get_wb_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:WBSTate \n
		Snippet: value: bool = driver.source.iq.get_wb_state() \n
		No command help available \n
			:return: wb_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:WBSTate?')
		return Conversions.str_to_bool(response)

	def set_wb_state(self, wb_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:WBSTate \n
		Snippet: driver.source.iq.set_wb_state(wb_state = False) \n
		No command help available \n
			:param wb_state: No help available
		"""
		param = Conversions.bool_to_str(wb_state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:WBSTate {param}')

	def clone(self) -> 'IqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
