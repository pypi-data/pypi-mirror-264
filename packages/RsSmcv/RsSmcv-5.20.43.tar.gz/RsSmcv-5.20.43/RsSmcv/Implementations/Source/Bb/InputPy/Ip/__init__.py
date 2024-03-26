from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpCls:
	"""Ip commands group definition. 8 total commands, 6 Subgroups, 0 group commands
	Repeated Capability: IpVersion, default value after init: IpVersion.Nr4"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ip", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_ipVersion_get', 'repcap_ipVersion_set', repcap.IpVersion.Nr4)

	def repcap_ipVersion_set(self, ipVersion: repcap.IpVersion) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IpVersion.Default
		Default value after init: IpVersion.Nr4"""
		self._cmd_group.set_repcap_enum_value(ipVersion)

	def repcap_ipVersion_get(self) -> repcap.IpVersion:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def alias(self):
		"""alias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alias'):
			from .Alias import AliasCls
			self._alias = AliasCls(self._core, self._cmd_group)
		return self._alias

	@property
	def igmp(self):
		"""igmp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_igmp'):
			from .Igmp import IgmpCls
			self._igmp = IgmpCls(self._core, self._cmd_group)
		return self._igmp

	@property
	def multicast(self):
		"""multicast commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_multicast'):
			from .Multicast import MulticastCls
			self._multicast = MulticastCls(self._core, self._cmd_group)
		return self._multicast

	@property
	def port(self):
		"""port commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_port'):
			from .Port import PortCls
			self._port = PortCls(self._core, self._cmd_group)
		return self._port

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'IpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
