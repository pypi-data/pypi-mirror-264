from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqModulatorCls:
	"""IqModulator commands group definition. 4 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqModulator", core, parent)

	@property
	def bband(self):
		"""bband commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bband'):
			from .Bband import BbandCls
			self._bband = BbandCls(self._core, self._cmd_group)
		return self._bband

	@property
	def iqModulator(self):
		"""iqModulator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqModulator'):
			from .IqModulator import IqModulatorCls
			self._iqModulator = IqModulatorCls(self._core, self._cmd_group)
		return self._iqModulator

	def get_full(self) -> bool:
		"""SCPI: CALibration<HW>:IQModulator:FULL \n
		Snippet: value: bool = driver.calibration.iqModulator.get_full() \n
		No command help available \n
			:return: full: No help available
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:IQModulator:FULL?')
		return Conversions.str_to_bool(response)

	def get_local(self) -> bool:
		"""SCPI: CALibration<HW>:IQModulator:LOCal \n
		Snippet: value: bool = driver.calibration.iqModulator.get_local() \n
		No command help available \n
			:return: local: No help available
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:IQModulator:LOCal?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'IqModulatorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqModulatorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
