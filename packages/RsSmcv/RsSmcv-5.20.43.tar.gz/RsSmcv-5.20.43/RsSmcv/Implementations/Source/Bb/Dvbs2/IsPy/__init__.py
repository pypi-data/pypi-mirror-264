from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IsPyCls:
	"""IsPy commands group definition. 5 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: InputStream, default value after init: InputStream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("isPy", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_inputStream_get', 'repcap_inputStream_set', repcap.InputStream.Nr1)

	def repcap_inputStream_set(self, inputStream: repcap.InputStream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to InputStream.Default
		Default value after init: InputStream.Nr1"""
		self._cmd_group.set_repcap_enum_value(inputStream)

	def repcap_inputStream_get(self) -> repcap.InputStream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def packetLength(self):
		"""packetLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_packetLength'):
			from .PacketLength import PacketLengthCls
			self._packetLength = PacketLengthCls(self._core, self._cmd_group)
		return self._packetLength

	@property
	def stuffing(self):
		"""stuffing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stuffing'):
			from .Stuffing import StuffingCls
			self._stuffing = StuffingCls(self._core, self._cmd_group)
		return self._stuffing

	@property
	def testSignal(self):
		"""testSignal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_testSignal'):
			from .TestSignal import TestSignalCls
			self._testSignal = TestSignalCls(self._core, self._cmd_group)
		return self._testSignal

	@property
	def useful(self):
		"""useful commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_useful'):
			from .Useful import UsefulCls
			self._useful = UsefulCls(self._core, self._cmd_group)
		return self._useful

	def clone(self) -> 'IsPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IsPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
