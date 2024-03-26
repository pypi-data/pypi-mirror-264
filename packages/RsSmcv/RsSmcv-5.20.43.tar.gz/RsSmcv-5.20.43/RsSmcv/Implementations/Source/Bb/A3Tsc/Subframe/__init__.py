from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubframeCls:
	"""Subframe commands group definition. 16 total commands, 12 Subgroups, 0 group commands
	Repeated Capability: Subframe, default value after init: Subframe.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subframe", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_subframe_get', 'repcap_subframe_set', repcap.Subframe.Nr1)

	def repcap_subframe_set(self, subframe: repcap.Subframe) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Subframe.Default
		Default value after init: Subframe.Nr1"""
		self._cmd_group.set_repcap_enum_value(subframe)

	def repcap_subframe_get(self) -> repcap.Subframe:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def carrier(self):
		"""carrier commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_carrier'):
			from .Carrier import CarrierCls
			self._carrier = CarrierCls(self._core, self._cmd_group)
		return self._carrier

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def fft(self):
		"""fft commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fft'):
			from .Fft import FftCls
			self._fft = FftCls(self._core, self._cmd_group)
		return self._fft

	@property
	def fil(self):
		"""fil commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fil'):
			from .Fil import FilCls
			self._fil = FilCls(self._core, self._cmd_group)
		return self._fil

	@property
	def guard(self):
		"""guard commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_guard'):
			from .Guard import GuardCls
			self._guard = GuardCls(self._core, self._cmd_group)
		return self._guard

	@property
	def mimo(self):
		"""mimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mimo'):
			from .Mimo import MimoCls
			self._mimo = MimoCls(self._core, self._cmd_group)
		return self._mimo

	@property
	def miso(self):
		"""miso commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_miso'):
			from .Miso import MisoCls
			self._miso = MisoCls(self._core, self._cmd_group)
		return self._miso

	@property
	def ndata(self):
		"""ndata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndata'):
			from .Ndata import NdataCls
			self._ndata = NdataCls(self._core, self._cmd_group)
		return self._ndata

	@property
	def pilot(self):
		"""pilot commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pilot'):
			from .Pilot import PilotCls
			self._pilot = PilotCls(self._core, self._cmd_group)
		return self._pilot

	@property
	def plp(self):
		"""plp commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_plp'):
			from .Plp import PlpCls
			self._plp = PlpCls(self._core, self._cmd_group)
		return self._plp

	@property
	def sbs(self):
		"""sbs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbs'):
			from .Sbs import SbsCls
			self._sbs = SbsCls(self._core, self._cmd_group)
		return self._sbs

	@property
	def used(self):
		"""used commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_used'):
			from .Used import UsedCls
			self._used = UsedCls(self._core, self._cmd_group)
		return self._used

	def clone(self) -> 'SubframeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubframeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
