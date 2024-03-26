from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def address(self):
		"""address commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_address'):
			from .Address import AddressCls
			self._address = AddressCls(self._core, self._cmd_group)
		return self._address

	@property
	def ping(self):
		"""ping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ping'):
			from .Ping import PingCls
			self._ping = PingCls(self._core, self._cmd_group)
		return self._ping

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	def clone(self) -> 'SourceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SourceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
