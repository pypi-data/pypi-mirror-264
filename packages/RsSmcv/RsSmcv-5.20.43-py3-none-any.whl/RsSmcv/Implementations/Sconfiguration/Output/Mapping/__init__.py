from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MappingCls:
	"""Mapping commands group definition. 6 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mapping", core, parent)

	@property
	def digital(self):
		"""digital commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import DigitalCls
			self._digital = DigitalCls(self._core, self._cmd_group)
		return self._digital

	@property
	def hsDigital(self):
		"""hsDigital commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsDigital'):
			from .HsDigital import HsDigitalCls
			self._hsDigital = HsDigitalCls(self._core, self._cmd_group)
		return self._hsDigital

	@property
	def iqOutput(self):
		"""iqOutput commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqOutput'):
			from .IqOutput import IqOutputCls
			self._iqOutput = IqOutputCls(self._core, self._cmd_group)
		return self._iqOutput

	@property
	def rf(self):
		"""rf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import RfCls
			self._rf = RfCls(self._core, self._cmd_group)
		return self._rf

	@property
	def stream(self):
		"""stream commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_stream'):
			from .Stream import StreamCls
			self._stream = StreamCls(self._core, self._cmd_group)
		return self._stream

	def clone(self) -> 'MappingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MappingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
