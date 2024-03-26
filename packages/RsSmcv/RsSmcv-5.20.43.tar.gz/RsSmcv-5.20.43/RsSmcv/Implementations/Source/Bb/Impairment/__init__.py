from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImpairmentCls:
	"""Impairment commands group definition. 16 total commands, 5 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("impairment", core, parent)

	@property
	def iqOutput(self):
		"""iqOutput commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOutput'):
			from .IqOutput import IqOutputCls
			self._iqOutput = IqOutputCls(self._core, self._cmd_group)
		return self._iqOutput

	@property
	def iqRatio(self):
		"""iqRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqRatio'):
			from .IqRatio import IqRatioCls
			self._iqRatio = IqRatioCls(self._core, self._cmd_group)
		return self._iqRatio

	@property
	def leakage(self):
		"""leakage commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_leakage'):
			from .Leakage import LeakageCls
			self._leakage = LeakageCls(self._core, self._cmd_group)
		return self._leakage

	@property
	def optimization(self):
		"""optimization commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_optimization'):
			from .Optimization import OptimizationCls
			self._optimization = OptimizationCls(self._core, self._cmd_group)
		return self._optimization

	@property
	def quadrature(self):
		"""quadrature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_quadrature'):
			from .Quadrature import QuadratureCls
			self._quadrature = QuadratureCls(self._core, self._cmd_group)
		return self._quadrature

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:DELay \n
		Snippet: value: float = driver.source.bb.impairment.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IMPairment:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:DELay \n
		Snippet: driver.source.bb.impairment.set_delay(delay = 1.0) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:IMPairment:DELay {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:STATe \n
		Snippet: value: bool = driver.source.bb.impairment.get_state() \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IMPairment:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:STATe \n
		Snippet: driver.source.bb.impairment.set_state(state = False) \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:IMPairment:STATe {param}')

	def clone(self) -> 'ImpairmentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ImpairmentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
