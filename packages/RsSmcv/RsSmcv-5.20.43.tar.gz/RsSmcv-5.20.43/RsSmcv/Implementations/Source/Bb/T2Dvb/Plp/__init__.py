from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PlpCls:
	"""Plp commands group definition. 29 total commands, 21 Subgroups, 0 group commands
	Repeated Capability: PhysicalLayerPipe, default value after init: PhysicalLayerPipe.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("plp", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_physicalLayerPipe_get', 'repcap_physicalLayerPipe_set', repcap.PhysicalLayerPipe.Nr1)

	def repcap_physicalLayerPipe_set(self, physicalLayerPipe: repcap.PhysicalLayerPipe) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PhysicalLayerPipe.Default
		Default value after init: PhysicalLayerPipe.Nr1"""
		self._cmd_group.set_repcap_enum_value(physicalLayerPipe)

	def repcap_physicalLayerPipe_get(self) -> repcap.PhysicalLayerPipe:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def blocks(self):
		"""blocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_blocks'):
			from .Blocks import BlocksCls
			self._blocks = BlocksCls(self._core, self._cmd_group)
		return self._blocks

	@property
	def cmType(self):
		"""cmType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmType'):
			from .CmType import CmTypeCls
			self._cmType = CmTypeCls(self._core, self._cmd_group)
		return self._cmType

	@property
	def constel(self):
		"""constel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_constel'):
			from .Constel import ConstelCls
			self._constel = ConstelCls(self._core, self._cmd_group)
		return self._constel

	@property
	def crotation(self):
		"""crotation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crotation'):
			from .Crotation import CrotationCls
			self._crotation = CrotationCls(self._core, self._cmd_group)
		return self._crotation

	@property
	def fecFrame(self):
		"""fecFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fecFrame'):
			from .FecFrame import FecFrameCls
			self._fecFrame = FecFrameCls(self._core, self._cmd_group)
		return self._fecFrame

	@property
	def frameIndex(self):
		"""frameIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frameIndex'):
			from .FrameIndex import FrameIndexCls
			self._frameIndex = FrameIndexCls(self._core, self._cmd_group)
		return self._frameIndex

	@property
	def group(self):
		"""group commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_group'):
			from .Group import GroupCls
			self._group = GroupCls(self._core, self._cmd_group)
		return self._group

	@property
	def ibs(self):
		"""ibs commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_ibs'):
			from .Ibs import IbsCls
			self._ibs = IbsCls(self._core, self._cmd_group)
		return self._ibs

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def inputPy(self):
		"""inputPy commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def issy(self):
		"""issy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_issy'):
			from .Issy import IssyCls
			self._issy = IssyCls(self._core, self._cmd_group)
		return self._issy

	@property
	def maxBlocks(self):
		"""maxBlocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maxBlocks'):
			from .MaxBlocks import MaxBlocksCls
			self._maxBlocks = MaxBlocksCls(self._core, self._cmd_group)
		return self._maxBlocks

	@property
	def npd(self):
		"""npd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npd'):
			from .Npd import NpdCls
			self._npd = NpdCls(self._core, self._cmd_group)
		return self._npd

	@property
	def oibPlp(self):
		"""oibPlp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oibPlp'):
			from .OibPlp import OibPlpCls
			self._oibPlp = OibPlpCls(self._core, self._cmd_group)
		return self._oibPlp

	@property
	def packetLength(self):
		"""packetLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_packetLength'):
			from .PacketLength import PacketLengthCls
			self._packetLength = PacketLengthCls(self._core, self._cmd_group)
		return self._packetLength

	@property
	def padFlag(self):
		"""padFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_padFlag'):
			from .PadFlag import PadFlagCls
			self._padFlag = PadFlagCls(self._core, self._cmd_group)
		return self._padFlag

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Rate import RateCls
			self._rate = RateCls(self._core, self._cmd_group)
		return self._rate

	@property
	def staFlag(self):
		"""staFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_staFlag'):
			from .StaFlag import StaFlagCls
			self._staFlag = StaFlagCls(self._core, self._cmd_group)
		return self._staFlag

	@property
	def til(self):
		"""til commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_til'):
			from .Til import TilCls
			self._til = TilCls(self._core, self._cmd_group)
		return self._til

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def useful(self):
		"""useful commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_useful'):
			from .Useful import UsefulCls
			self._useful = UsefulCls(self._core, self._cmd_group)
		return self._useful

	def clone(self) -> 'PlpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PlpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
