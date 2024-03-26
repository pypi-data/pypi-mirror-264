from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BCls:
	"""B commands group definition. 20 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("b", core, parent)

	@property
	def list1(self):
		"""list1 commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_list1'):
			from .List1 import List1Cls
			self._list1 = List1Cls(self._core, self._cmd_group)
		return self._list1

	@property
	def list2(self):
		"""list2 commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_list2'):
			from .List2 import List2Cls
			self._list2 = List2Cls(self._core, self._cmd_group)
		return self._list2

	@property
	def list3(self):
		"""list3 commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_list3'):
			from .List3 import List3Cls
			self._list3 = List3Cls(self._core, self._cmd_group)
		return self._list3

	@property
	def list4(self):
		"""list4 commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_list4'):
			from .List4 import List4Cls
			self._list4 = List4Cls(self._core, self._cmd_group)
		return self._list4

	@property
	def list5(self):
		"""list5 commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_list5'):
			from .List5 import List5Cls
			self._list5 = List5Cls(self._core, self._cmd_group)
		return self._list5

	def clone(self) -> 'BCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
