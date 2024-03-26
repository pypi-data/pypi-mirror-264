from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def isPy(self):
		"""isPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isPy'):
			from .IsPy import IsPyCls
			self._isPy = IsPyCls(self._core, self._cmd_group)
		return self._isPy

	# noinspection PyTypeChecker
	def get_value(self) -> enums.CodingInputSignalSource:
		"""SCPI: [SOURce<HW>]:BB:DVBS2:SOURce \n
		Snippet: value: enums.CodingInputSignalSource = driver.source.bb.dvbs2.source.get_value() \n
		Sets the modulation source for the input signal. \n
			:return: source: EXTernal| TSPLayer| TESTsignal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBS2:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.CodingInputSignalSource)

	def set_value(self, source: enums.CodingInputSignalSource) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBS2:SOURce \n
		Snippet: driver.source.bb.dvbs2.source.set_value(source = enums.CodingInputSignalSource.EXTernal) \n
		Sets the modulation source for the input signal. \n
			:param source: EXTernal| TSPLayer| TESTsignal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.CodingInputSignalSource)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBS2:SOURce {param}')

	def clone(self) -> 'SourceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SourceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
