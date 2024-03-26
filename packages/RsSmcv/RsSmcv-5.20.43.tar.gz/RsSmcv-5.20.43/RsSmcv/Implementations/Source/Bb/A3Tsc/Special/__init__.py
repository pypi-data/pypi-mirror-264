from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpecialCls:
	"""Special commands group definition. 6 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("special", core, parent)

	@property
	def alp(self):
		"""alp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alp'):
			from .Alp import AlpCls
			self._alp = AlpCls(self._core, self._cmd_group)
		return self._alp

	@property
	def bootstrap(self):
		"""bootstrap commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bootstrap'):
			from .Bootstrap import BootstrapCls
			self._bootstrap = BootstrapCls(self._core, self._cmd_group)
		return self._bootstrap

	@property
	def settings(self):
		"""settings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_settings'):
			from .Settings import SettingsCls
			self._settings = SettingsCls(self._core, self._cmd_group)
		return self._settings

	@property
	def stl(self):
		"""stl commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_stl'):
			from .Stl import StlCls
			self._stl = StlCls(self._core, self._cmd_group)
		return self._stl

	def clone(self) -> 'SpecialCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpecialCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
