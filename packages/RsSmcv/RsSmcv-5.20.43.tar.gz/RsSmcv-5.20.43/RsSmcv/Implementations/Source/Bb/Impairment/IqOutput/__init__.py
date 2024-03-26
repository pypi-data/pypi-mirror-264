from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqOutputCls:
	"""IqOutput commands group definition. 8 total commands, 7 Subgroups, 0 group commands
	Repeated Capability: IqConnector, default value after init: IqConnector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqOutput", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_iqConnector_get', 'repcap_iqConnector_set', repcap.IqConnector.Nr1)

	def repcap_iqConnector_set(self, iqConnector: repcap.IqConnector) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IqConnector.Default
		Default value after init: IqConnector.Nr1"""
		self._cmd_group.set_repcap_enum_value(iqConnector)

	def repcap_iqConnector_get(self) -> repcap.IqConnector:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def iqRatio(self):
		"""iqRatio commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqRatio'):
			from .IqRatio import IqRatioCls
			self._iqRatio = IqRatioCls(self._core, self._cmd_group)
		return self._iqRatio

	@property
	def leakage(self):
		"""leakage commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_leakage'):
			from .Leakage import LeakageCls
			self._leakage = LeakageCls(self._core, self._cmd_group)
		return self._leakage

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Poffset import PoffsetCls
			self._poffset = PoffsetCls(self._core, self._cmd_group)
		return self._poffset

	@property
	def quadrature(self):
		"""quadrature commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_quadrature'):
			from .Quadrature import QuadratureCls
			self._quadrature = QuadratureCls(self._core, self._cmd_group)
		return self._quadrature

	@property
	def skew(self):
		"""skew commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_skew'):
			from .Skew import SkewCls
			self._skew = SkewCls(self._core, self._cmd_group)
		return self._skew

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'IqOutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqOutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
