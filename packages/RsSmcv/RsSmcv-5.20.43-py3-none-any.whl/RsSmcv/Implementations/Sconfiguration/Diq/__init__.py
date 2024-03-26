from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DiqCls:
	"""Diq commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("diq", core, parent)

	@property
	def bbMm1(self):
		"""bbMm1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbMm1'):
			from .BbMm1 import BbMm1Cls
			self._bbMm1 = BbMm1Cls(self._core, self._cmd_group)
		return self._bbMm1

	@property
	def bbMm2(self):
		"""bbMm2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbMm2'):
			from .BbMm2 import BbMm2Cls
			self._bbMm2 = BbMm2Cls(self._core, self._cmd_group)
		return self._bbMm2

	def clone(self) -> 'DiqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DiqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
