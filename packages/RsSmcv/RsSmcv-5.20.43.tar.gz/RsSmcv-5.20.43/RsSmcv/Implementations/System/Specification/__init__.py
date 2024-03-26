from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpecificationCls:
	"""Specification commands group definition. 7 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("specification", core, parent)

	@property
	def identification(self):
		"""identification commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_identification'):
			from .Identification import IdentificationCls
			self._identification = IdentificationCls(self._core, self._cmd_group)
		return self._identification

	@property
	def version(self):
		"""version commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_version'):
			from .Version import VersionCls
			self._version = VersionCls(self._core, self._cmd_group)
		return self._version

	def get_parameter(self) -> List[float]:
		"""SCPI: SYSTem:SPECification:PARameter \n
		Snippet: value: List[float] = driver.system.specification.get_parameter() \n
		Retrieves data sheet information for a specific parameter. \n
			:return: val_list: float Comma-separated list with the specified and, if available, the typical value of the parameter, as specified in the data sheet.
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SYSTem:SPECification:PARameter?')
		return response

	def get_value(self) -> List[float]:
		"""SCPI: SYSTem:SPECification \n
		Snippet: value: List[float] = driver.system.specification.get_value() \n
		Retrieves data sheet information for a specific parameter. \n
			:return: val_list: float Comma-separated list with the specified and, if available, the typical value of the parameter, as specified in the data sheet.
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SYSTem:SPECification?')
		return response

	def clone(self) -> 'SpecificationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpecificationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
