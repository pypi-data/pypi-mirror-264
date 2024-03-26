from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SbsCls:
	"""Sbs commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sbs", core, parent)

	@property
	def first(self):
		"""first commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_first'):
			from .First import FirstCls
			self._first = FirstCls(self._core, self._cmd_group)
		return self._first

	@property
	def last(self):
		"""last commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_last'):
			from .Last import LastCls
			self._last = LastCls(self._core, self._cmd_group)
		return self._last

	@property
	def null(self):
		"""null commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_null'):
			from .Null import NullCls
			self._null = NullCls(self._core, self._cmd_group)
		return self._null

	def clone(self) -> 'SbsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SbsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
