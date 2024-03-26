from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbinCls:
	"""Bbin commands group definition. 35 total commands, 8 Subgroups, 12 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bbin", core, parent)

	@property
	def alevel(self):
		"""alevel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_alevel'):
			from .Alevel import AlevelCls
			self._alevel = AlevelCls(self._core, self._cmd_group)
		return self._alevel

	@property
	def channel(self):
		"""channel commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def digital(self):
		"""digital commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import DigitalCls
			self._digital = DigitalCls(self._core, self._cmd_group)
		return self._digital

	@property
	def iqswap(self):
		"""iqswap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqswap'):
			from .Iqswap import IqswapCls
			self._iqswap = IqswapCls(self._core, self._cmd_group)
		return self._iqswap

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def oload(self):
		"""oload commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_oload'):
			from .Oload import OloadCls
			self._oload = OloadCls(self._core, self._cmd_group)
		return self._oload

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	def get_cdevice(self) -> str:
		"""SCPI: [SOURce<HW>]:BBIN:CDEVice \n
		Snippet: value: str = driver.source.bbin.get_cdevice() \n
		Indicates the ID of an externally connected Rohde & Schwarz Instrument or Rohde & Schwarz device. \n
			:return: cdevice: string 'None' - no device is connected.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:CDEVice?')
		return trim_str_response(response)

	def get_cfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:CFACtor \n
		Snippet: value: float = driver.source.bbin.get_cfactor() \n
		No command help available \n
			:return: cfactor: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:CFACtor?')
		return Conversions.str_to_float(response)

	def set_cfactor(self, cfactor: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:CFACtor \n
		Snippet: driver.source.bbin.set_cfactor(cfactor = 1.0) \n
		No command help available \n
			:param cfactor: No help available
		"""
		param = Conversions.decimal_value_to_str(cfactor)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:CFACtor {param}')

	def get_foffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:FOFFset \n
		Snippet: value: float = driver.source.bbin.get_foffset() \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:return: foffset: float Range: depends on the installed options , Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, foffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:FOFFset \n
		Snippet: driver.source.bbin.set_foffset(foffset = 1.0) \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:param foffset: float Range: depends on the installed options , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(foffset)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:FOFFset {param}')

	def get_gimbalance(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:GIMBalance \n
		Snippet: value: float = driver.source.bbin.get_gimbalance() \n
		No command help available \n
			:return: gimbalance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:GIMBalance?')
		return Conversions.str_to_float(response)

	def set_gimbalance(self, gimbalance: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:GIMBalance \n
		Snippet: driver.source.bbin.set_gimbalance(gimbalance = 1.0) \n
		No command help available \n
			:param gimbalance: No help available
		"""
		param = Conversions.decimal_value_to_str(gimbalance)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:GIMBalance {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AnalogDigital:
		"""SCPI: [SOURce<HW>]:BBIN:MODE \n
		Snippet: value: enums.AnalogDigital = driver.source.bbin.get_mode() \n
		Defines that a digital external signal is applied. \n
			:return: mode: DIGital
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AnalogDigital)

	def set_mode(self, mode: enums.AnalogDigital) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:MODE \n
		Snippet: driver.source.bbin.set_mode(mode = enums.AnalogDigital.ANALog) \n
		Defines that a digital external signal is applied. \n
			:param mode: DIGital
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AnalogDigital)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:MODE {param}')

	def get_mperiod(self) -> int:
		"""SCPI: [SOURce<HW>]:BBIN:MPERiod \n
		Snippet: value: int = driver.source.bbin.get_mperiod() \n
		Sets the recording duration for measuring the baseband input signal by executed [:SOURce<hw>]:BBIN:ALEVel:EXECute. \n
			:return: mperiod: integer Range: 1 to 32, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:MPERiod?')
		return Conversions.str_to_int(response)

	def set_mperiod(self, mperiod: int) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:MPERiod \n
		Snippet: driver.source.bbin.set_mperiod(mperiod = 1) \n
		Sets the recording duration for measuring the baseband input signal by executed [:SOURce<hw>]:BBIN:ALEVel:EXECute. \n
			:param mperiod: integer Range: 1 to 32, Unit: s
		"""
		param = Conversions.decimal_value_to_str(mperiod)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:MPERiod {param}')

	def get_odelay(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:ODELay \n
		Snippet: value: float = driver.source.bbin.get_odelay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:ODELay?')
		return Conversions.str_to_float(response)

	def set_odelay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:ODELay \n
		Snippet: driver.source.bbin.set_odelay(delay = 1.0) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:ODELay {param}')

	def get_pgain(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:PGAin \n
		Snippet: value: float = driver.source.bbin.get_pgain() \n
		No command help available \n
			:return: pgain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:PGAin?')
		return Conversions.str_to_float(response)

	def set_pgain(self, pgain: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:PGAin \n
		Snippet: driver.source.bbin.set_pgain(pgain = 1.0) \n
		No command help available \n
			:param pgain: No help available
		"""
		param = Conversions.decimal_value_to_str(pgain)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:PGAin {param}')

	def get_poffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:POFFset \n
		Snippet: value: float = driver.source.bbin.get_poffset() \n
		Sets the relative phase offset for the external baseband signal. \n
			:return: poffset: float Range: -999.99 to 999.99, Unit: DEG
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, poffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:POFFset \n
		Snippet: driver.source.bbin.set_poffset(poffset = 1.0) \n
		Sets the relative phase offset for the external baseband signal. \n
			:param poffset: float Range: -999.99 to 999.99, Unit: DEG
		"""
		param = Conversions.decimal_value_to_str(poffset)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:POFFset {param}')

	# noinspection PyTypeChecker
	def get_route(self) -> enums.PathUniCodBbinA:
		"""SCPI: [SOURce<HW>]:BBIN:ROUTe \n
		Snippet: value: enums.PathUniCodBbinA = driver.source.bbin.get_route() \n
		Selects the signal route for the internal/external baseband signal. \n
			:return: route: A
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:ROUTe?')
		return Conversions.str_to_scalar_enum(response, enums.PathUniCodBbinA)

	def set_route(self, route: enums.PathUniCodBbinA) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:ROUTe \n
		Snippet: driver.source.bbin.set_route(route = enums.PathUniCodBbinA.A) \n
		Selects the signal route for the internal/external baseband signal. \n
			:param route: A
		"""
		param = Conversions.enum_scalar_to_str(route, enums.PathUniCodBbinA)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:ROUTe {param}')

	def get_skew(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:SKEW \n
		Snippet: value: float = driver.source.bbin.get_skew() \n
		No command help available \n
			:return: skew: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:SKEW?')
		return Conversions.str_to_float(response)

	def set_skew(self, skew: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:SKEW \n
		Snippet: driver.source.bbin.set_skew(skew = 1.0) \n
		No command help available \n
			:param skew: No help available
		"""
		param = Conversions.decimal_value_to_str(skew)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:SKEW {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BBIN:STATe \n
		Snippet: value: bool = driver.source.bbin.get_state() \n
		Enables feeding of an external digital signal into the signal path. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:STATe \n
		Snippet: driver.source.bbin.set_state(state = False) \n
		Enables feeding of an external digital signal into the signal path. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:STATe {param}')

	def clone(self) -> 'BbinCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbinCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
