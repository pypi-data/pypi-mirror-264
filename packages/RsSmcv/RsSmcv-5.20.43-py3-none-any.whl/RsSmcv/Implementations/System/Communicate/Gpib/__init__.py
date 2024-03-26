from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GpibCls:
	"""Gpib commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gpib", core, parent)

	@property
	def self(self):
		"""self commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_self'):
			from .Self import SelfCls
			self._self = SelfCls(self._core, self._cmd_group)
		return self._self

	# noinspection PyTypeChecker
	def get_lterminator(self) -> enums.IecTermMode:
		"""SCPI: SYSTem:COMMunicate:GPIB:LTERminator \n
		Snippet: value: enums.IecTermMode = driver.system.communicate.gpib.get_lterminator() \n
		No command help available \n
			:return: lterminator: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:GPIB:LTERminator?')
		return Conversions.str_to_scalar_enum(response, enums.IecTermMode)

	def set_lterminator(self, lterminator: enums.IecTermMode) -> None:
		"""SCPI: SYSTem:COMMunicate:GPIB:LTERminator \n
		Snippet: driver.system.communicate.gpib.set_lterminator(lterminator = enums.IecTermMode.EOI) \n
		No command help available \n
			:param lterminator: No help available
		"""
		param = Conversions.enum_scalar_to_str(lterminator, enums.IecTermMode)
		self._core.io.write(f'SYSTem:COMMunicate:GPIB:LTERminator {param}')

	def get_resource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:GPIB:RESource \n
		Snippet: value: str = driver.system.communicate.gpib.get_resource() \n
		No command help available \n
			:return: resource: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:GPIB:RESource?')
		return trim_str_response(response)

	def clone(self) -> 'GpibCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GpibCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
