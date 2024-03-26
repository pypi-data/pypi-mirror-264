from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbCls:
	"""Bb commands group definition. 1134 total commands, 26 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bb", core, parent)

	@property
	def a3Tsc(self):
		"""a3Tsc commands group. 14 Sub-classes, 14 commands."""
		if not hasattr(self, '_a3Tsc'):
			from .A3Tsc import A3TscCls
			self._a3Tsc = A3TscCls(self._core, self._cmd_group)
		return self._a3Tsc

	@property
	def arbitrary(self):
		"""arbitrary commands group. 9 Sub-classes, 2 commands."""
		if not hasattr(self, '_arbitrary'):
			from .Arbitrary import ArbitraryCls
			self._arbitrary = ArbitraryCls(self._core, self._cmd_group)
		return self._arbitrary

	@property
	def atsm(self):
		"""atsm commands group. 9 Sub-classes, 17 commands."""
		if not hasattr(self, '_atsm'):
			from .Atsm import AtsmCls
			self._atsm = AtsmCls(self._core, self._cmd_group)
		return self._atsm

	@property
	def coder(self):
		"""coder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coder'):
			from .Coder import CoderCls
			self._coder = CoderCls(self._core, self._cmd_group)
		return self._coder

	@property
	def dab(self):
		"""dab commands group. 11 Sub-classes, 7 commands."""
		if not hasattr(self, '_dab'):
			from .Dab import DabCls
			self._dab = DabCls(self._core, self._cmd_group)
		return self._dab

	@property
	def drm(self):
		"""drm commands group. 3 Sub-classes, 12 commands."""
		if not hasattr(self, '_drm'):
			from .Drm import DrmCls
			self._drm = DrmCls(self._core, self._cmd_group)
		return self._drm

	@property
	def dtmb(self):
		"""dtmb commands group. 8 Sub-classes, 16 commands."""
		if not hasattr(self, '_dtmb'):
			from .Dtmb import DtmbCls
			self._dtmb = DtmbCls(self._core, self._cmd_group)
		return self._dtmb

	@property
	def dvbc(self):
		"""dvbc commands group. 4 Sub-classes, 14 commands."""
		if not hasattr(self, '_dvbc'):
			from .Dvbc import DvbcCls
			self._dvbc = DvbcCls(self._core, self._cmd_group)
		return self._dvbc

	@property
	def dvbs2(self):
		"""dvbs2 commands group. 9 Sub-classes, 9 commands."""
		if not hasattr(self, '_dvbs2'):
			from .Dvbs2 import Dvbs2Cls
			self._dvbs2 = Dvbs2Cls(self._core, self._cmd_group)
		return self._dvbs2

	@property
	def dvbs(self):
		"""dvbs commands group. 4 Sub-classes, 15 commands."""
		if not hasattr(self, '_dvbs'):
			from .Dvbs import DvbsCls
			self._dvbs = DvbsCls(self._core, self._cmd_group)
		return self._dvbs

	@property
	def dvbt(self):
		"""dvbt commands group. 19 Sub-classes, 9 commands."""
		if not hasattr(self, '_dvbt'):
			from .Dvbt import DvbtCls
			self._dvbt = DvbtCls(self._core, self._cmd_group)
		return self._dvbt

	@property
	def general(self):
		"""general commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_general'):
			from .General import GeneralCls
			self._general = GeneralCls(self._core, self._cmd_group)
		return self._general

	@property
	def graphics(self):
		"""graphics commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_graphics'):
			from .Graphics import GraphicsCls
			self._graphics = GraphicsCls(self._core, self._cmd_group)
		return self._graphics

	@property
	def impairment(self):
		"""impairment commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_impairment'):
			from .Impairment import ImpairmentCls
			self._impairment = ImpairmentCls(self._core, self._cmd_group)
		return self._impairment

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def inputPy(self):
		"""inputPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def isdbt(self):
		"""isdbt commands group. 17 Sub-classes, 14 commands."""
		if not hasattr(self, '_isdbt'):
			from .Isdbt import IsdbtCls
			self._isdbt = IsdbtCls(self._core, self._cmd_group)
		return self._isdbt

	@property
	def j83B(self):
		"""j83B commands group. 5 Sub-classes, 14 commands."""
		if not hasattr(self, '_j83B'):
			from .J83B import J83BCls
			self._j83B = J83BCls(self._core, self._cmd_group)
		return self._j83B

	@property
	def lora(self):
		"""lora commands group. 7 Sub-classes, 6 commands."""
		if not hasattr(self, '_lora'):
			from .Lora import LoraCls
			self._lora = LoraCls(self._core, self._cmd_group)
		return self._lora

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Path import PathCls
			self._path = PathCls(self._core, self._cmd_group)
		return self._path

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def progress(self):
		"""progress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_progress'):
			from .Progress import ProgressCls
			self._progress = ProgressCls(self._core, self._cmd_group)
		return self._progress

	@property
	def radio(self):
		"""radio commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_radio'):
			from .Radio import RadioCls
			self._radio = RadioCls(self._core, self._cmd_group)
		return self._radio

	@property
	def t2Dvb(self):
		"""t2Dvb commands group. 15 Sub-classes, 18 commands."""
		if not hasattr(self, '_t2Dvb'):
			from .T2Dvb import T2DvbCls
			self._t2Dvb = T2DvbCls(self._core, self._cmd_group)
		return self._t2Dvb

	@property
	def tdmb(self):
		"""tdmb commands group. 9 Sub-classes, 7 commands."""
		if not hasattr(self, '_tdmb'):
			from .Tdmb import TdmbCls
			self._tdmb = TdmbCls(self._core, self._cmd_group)
		return self._tdmb

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	def get_cfactor(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:CFACtor \n
		Snippet: value: float = driver.source.bb.get_cfactor() \n
		Queries the crest factor of the baseband signal. \n
			:return: cfactor: float Range: 0 to 100, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:CFACtor?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_configuration(self) -> enums.BbConfig:
		"""SCPI: [SOURce]:BB:CONFiguration \n
		Snippet: value: enums.BbConfig = driver.source.bb.get_configuration() \n
		No command help available \n
			:return: configuration: No help available
		"""
		response = self._core.io.query_str('SOURce:BB:CONFiguration?')
		return Conversions.str_to_scalar_enum(response, enums.BbConfig)

	def set_configuration(self, configuration: enums.BbConfig) -> None:
		"""SCPI: [SOURce]:BB:CONFiguration \n
		Snippet: driver.source.bb.set_configuration(configuration = enums.BbConfig.NORMal) \n
		No command help available \n
			:param configuration: No help available
		"""
		param = Conversions.enum_scalar_to_str(configuration, enums.BbConfig)
		self._core.io.write(f'SOURce:BB:CONFiguration {param}')

	def get_foffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: value: float = driver.source.bb.get_foffset() \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:return: foffset: float Range: depends on the installed options , Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, foffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: driver.source.bb.set_foffset(foffset = 1.0) \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:param foffset: float Range: depends on the installed options , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(foffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:FOFFset {param}')

	# noinspection PyTypeChecker
	def get_iq_gain(self) -> enums.IqGain:
		"""SCPI: [SOURce<HW>]:BB:IQGain \n
		Snippet: value: enums.IqGain = driver.source.bb.get_iq_gain() \n
		No command help available \n
			:return: ipartq_gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IQGain?')
		return Conversions.str_to_scalar_enum(response, enums.IqGain)

	def set_iq_gain(self, ipartq_gain: enums.IqGain) -> None:
		"""SCPI: [SOURce<HW>]:BB:IQGain \n
		Snippet: driver.source.bb.set_iq_gain(ipartq_gain = enums.IqGain.DB0) \n
		No command help available \n
			:param ipartq_gain: No help available
		"""
		param = Conversions.enum_scalar_to_str(ipartq_gain, enums.IqGain)
		self._core.io.write(f'SOURce<HwInstance>:BB:IQGain {param}')

	def get_pgain(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:PGAin \n
		Snippet: value: float = driver.source.bb.get_pgain() \n
		No command help available \n
			:return: pgain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PGAin?')
		return Conversions.str_to_float(response)

	def set_pgain(self, pgain: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:PGAin \n
		Snippet: driver.source.bb.set_pgain(pgain = 1.0) \n
		No command help available \n
			:param pgain: No help available
		"""
		param = Conversions.decimal_value_to_str(pgain)
		self._core.io.write(f'SOURce<HwInstance>:BB:PGAin {param}')

	def get_poffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: value: float = driver.source.bb.get_poffset() \n
		Sets the relative phase offset for the selected baseband signal. \n
			:return: poffset: float Range: 0 to 359.9, Unit: DEG
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, poffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: driver.source.bb.set_poffset(poffset = 1.0) \n
		Sets the relative phase offset for the selected baseband signal. \n
			:param poffset: float Range: 0 to 359.9, Unit: DEG
		"""
		param = Conversions.decimal_value_to_str(poffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:POFFset {param}')

	# noinspection PyTypeChecker
	def get_route(self) -> enums.PathUniCodBbin:
		"""SCPI: [SOURce<HW>]:BB:ROUTe \n
		Snippet: value: enums.PathUniCodBbin = driver.source.bb.get_route() \n
		Selects the signal route for the internal/external baseband signal. \n
			:return: route: A
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ROUTe?')
		return Conversions.str_to_scalar_enum(response, enums.PathUniCodBbin)

	def set_route(self, route: enums.PathUniCodBbin) -> None:
		"""SCPI: [SOURce<HW>]:BB:ROUTe \n
		Snippet: driver.source.bb.set_route(route = enums.PathUniCodBbin.A) \n
		Selects the signal route for the internal/external baseband signal. \n
			:param route: A
		"""
		param = Conversions.enum_scalar_to_str(route, enums.PathUniCodBbin)
		self._core.io.write(f'SOURce<HwInstance>:BB:ROUTe {param}')

	def clone(self) -> 'BbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
