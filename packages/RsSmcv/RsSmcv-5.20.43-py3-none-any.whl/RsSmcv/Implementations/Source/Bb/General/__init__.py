from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GeneralCls:
	"""General commands group definition. 23 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("general", core, parent)

	@property
	def am(self):
		"""am commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_am'):
			from .Am import AmCls
			self._am = AmCls(self._core, self._cmd_group)
		return self._am

	@property
	def fm(self):
		"""fm commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import FmCls
			self._fm = FmCls(self._core, self._cmd_group)
		return self._fm

	@property
	def pm(self):
		"""pm commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_pm'):
			from .Pm import PmCls
			self._pm = PmCls(self._core, self._cmd_group)
		return self._pm

	@property
	def pulm(self):
		"""pulm commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_pulm'):
			from .Pulm import PulmCls
			self._pulm = PulmCls(self._core, self._cmd_group)
		return self._pulm

	def clone(self) -> 'GeneralCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GeneralCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
