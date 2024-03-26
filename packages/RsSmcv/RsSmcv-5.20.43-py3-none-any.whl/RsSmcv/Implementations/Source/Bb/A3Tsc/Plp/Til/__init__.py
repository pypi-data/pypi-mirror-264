from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TilCls:
	"""Til commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("til", core, parent)

	@property
	def blocks(self):
		"""blocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_blocks'):
			from .Blocks import BlocksCls
			self._blocks = BlocksCls(self._core, self._cmd_group)
		return self._blocks

	@property
	def cil(self):
		"""cil commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cil'):
			from .Cil import CilCls
			self._cil = CilCls(self._core, self._cmd_group)
		return self._cil

	@property
	def depth(self):
		"""depth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_depth'):
			from .Depth import DepthCls
			self._depth = DepthCls(self._core, self._cmd_group)
		return self._depth

	@property
	def extended(self):
		"""extended commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_extended'):
			from .Extended import ExtendedCls
			self._extended = ExtendedCls(self._core, self._cmd_group)
		return self._extended

	@property
	def inter(self):
		"""inter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inter'):
			from .Inter import InterCls
			self._inter = InterCls(self._core, self._cmd_group)
		return self._inter

	@property
	def maxBlocks(self):
		"""maxBlocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maxBlocks'):
			from .MaxBlocks import MaxBlocksCls
			self._maxBlocks = MaxBlocksCls(self._core, self._cmd_group)
		return self._maxBlocks

	@property
	def ntiBlocks(self):
		"""ntiBlocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntiBlocks'):
			from .NtiBlocks import NtiBlocksCls
			self._ntiBlocks = NtiBlocksCls(self._core, self._cmd_group)
		return self._ntiBlocks

	@property
	def til(self):
		"""til commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_til'):
			from .Til import TilCls
			self._til = TilCls(self._core, self._cmd_group)
		return self._til

	def clone(self) -> 'TilCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TilCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
