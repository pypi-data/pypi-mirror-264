from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ServoingCls:
	"""Servoing commands group definition. 5 total commands, 0 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("servoing", core, parent)

	# noinspection PyTypeChecker
	class SetStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Target: float: No parameter help available
			- Start: enums.Test: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Target'),
			ArgStruct.scalar_enum('Start', enums.Test)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Target: float = None
			self.Start: enums.Test = None

	def get_set(self) -> SetStruct:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:SET \n
		Snippet: value: SetStruct = driver.source.power.servoing.get_set() \n
		No command help available \n
			:return: structure: for return value, see the help for SetStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:POWer:SERVoing:SET?', self.__class__.SetStruct())

	def get_target(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:TARGet \n
		Snippet: value: float = driver.source.power.servoing.get_target() \n
		No command help available \n
			:return: target_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SERVoing:TARGet?')
		return Conversions.str_to_float(response)

	def set_target(self, target_level: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:TARGet \n
		Snippet: driver.source.power.servoing.set_target(target_level = 1.0) \n
		No command help available \n
			:param target_level: No help available
		"""
		param = Conversions.decimal_value_to_str(target_level)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SERVoing:TARGet {param}')

	# noinspection PyTypeChecker
	def get_test(self) -> enums.Test:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:TEST \n
		Snippet: value: enums.Test = driver.source.power.servoing.get_test() \n
		No command help available \n
			:return: start: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SERVoing:TEST?')
		return Conversions.str_to_scalar_enum(response, enums.Test)

	def get_tolerance(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:TOLerance \n
		Snippet: value: float = driver.source.power.servoing.get_tolerance() \n
		No command help available \n
			:return: tolerance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SERVoing:TOLerance?')
		return Conversions.str_to_float(response)

	def set_tolerance(self, tolerance: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:TOLerance \n
		Snippet: driver.source.power.servoing.set_tolerance(tolerance = 1.0) \n
		No command help available \n
			:param tolerance: No help available
		"""
		param = Conversions.decimal_value_to_str(tolerance)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SERVoing:TOLerance {param}')

	def get_tracking(self) -> bool:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:TRACking \n
		Snippet: value: bool = driver.source.power.servoing.get_tracking() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SERVoing:TRACking?')
		return Conversions.str_to_bool(response)

	def set_tracking(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SERVoing:TRACking \n
		Snippet: driver.source.power.servoing.set_tracking(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SERVoing:TRACking {param}')
