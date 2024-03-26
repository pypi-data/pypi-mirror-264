from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PolynomialCls:
	"""Polynomial commands group definition. 4 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("polynomial", core, parent)

	@property
	def coefficients(self):
		"""coefficients commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_coefficients'):
			from .Coefficients import CoefficientsCls
			self._coefficients = CoefficientsCls(self._core, self._cmd_group)
		return self._coefficients

	def clone(self) -> 'PolynomialCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PolynomialCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
