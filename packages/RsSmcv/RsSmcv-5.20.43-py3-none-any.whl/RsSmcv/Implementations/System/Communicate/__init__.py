from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CommunicateCls:
	"""Communicate commands group definition. 33 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("communicate", core, parent)

	@property
	def bb(self):
		"""bb commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	@property
	def bcIp(self):
		"""bcIp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bcIp'):
			from .BcIp import BcIpCls
			self._bcIp = BcIpCls(self._core, self._cmd_group)
		return self._bcIp

	@property
	def gpib(self):
		"""gpib commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_gpib'):
			from .Gpib import GpibCls
			self._gpib = GpibCls(self._core, self._cmd_group)
		return self._gpib

	@property
	def hislip(self):
		"""hislip commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hislip'):
			from .Hislip import HislipCls
			self._hislip = HislipCls(self._core, self._cmd_group)
		return self._hislip

	@property
	def network(self):
		"""network commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_network'):
			from .Network import NetworkCls
			self._network = NetworkCls(self._core, self._cmd_group)
		return self._network

	@property
	def pciExpress(self):
		"""pciExpress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pciExpress'):
			from .PciExpress import PciExpressCls
			self._pciExpress = PciExpressCls(self._core, self._cmd_group)
		return self._pciExpress

	@property
	def scpi(self):
		"""scpi commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scpi'):
			from .Scpi import ScpiCls
			self._scpi = ScpiCls(self._core, self._cmd_group)
		return self._scpi

	@property
	def serial(self):
		"""serial commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_serial'):
			from .Serial import SerialCls
			self._serial = SerialCls(self._core, self._cmd_group)
		return self._serial

	@property
	def socket(self):
		"""socket commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_socket'):
			from .Socket import SocketCls
			self._socket = SocketCls(self._core, self._cmd_group)
		return self._socket

	def clone(self) -> 'CommunicateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CommunicateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
