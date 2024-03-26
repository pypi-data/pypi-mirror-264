from typing import ClassVar, List

from .Internal.Core import Core
from .Internal.InstrumentErrors import RsInstrException
from .Internal.CommandsGroup import CommandsGroup
from .Internal.VisaSession import VisaSession
from datetime import datetime, timedelta
from .Internal import Conversions
from . import repcap
from .Internal.RepeatedCapability import RepeatedCapability


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsSmcv:
	"""1998 total commands, 24 Subgroups, 4 group commands"""
	_driver_options = "SupportedInstrModels = SMCV/SMW/SMBV/SMA, SupportedIdnPatterns = SMCV/SMBV/SMW/SMA, SimulationIdnString = 'Rohde&Schwarz,SMCV100B,100001,5.20.43.0018'"
	_global_logging_relative_timestamp: ClassVar[datetime] = None
	_global_logging_target_stream: ClassVar = None

	def __init__(self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
		"""Initializes new RsSmcv session. \n
		Parameter options tokens examples:
			- ``Simulate=True`` - starts the session in simulation mode. Default: ``False``
			- ``SelectVisa=socket`` - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			- ``SelectVisa=rs`` - forces usage of RohdeSchwarz Visa
			- ``SelectVisa=ivi`` - forces usage of National Instruments Visa
			- ``QueryInstrumentStatus = False`` - same as ``driver.utilities.instrument_status_checking = False``. Default: ``True``
			- ``WriteDelay = 20, ReadDelay = 5`` - Introduces delay of 20ms before each write and 5ms before each read. Default: ``0ms`` for both
			- ``OpcWaitMode = OpcQuery`` - mode for all the opc-synchronised write/reads. Other modes: StbPolling, StbPollingSlow, StbPollingSuperSlow. Default: ``StbPolling``
			- ``AddTermCharToWriteBinBLock = True`` - Adds one additional LF to the end of the binary data (some instruments require that). Default: ``False``
			- ``AssureWriteWithTermChar = True`` - Makes sure each command/query is terminated with termination character. Default: Interface dependent
			- ``TerminationCharacter = "\\r"`` - Sets the termination character for reading. Default: ``\\n`` (LineFeed or LF)
			- ``DataChunkSize = 10E3`` - Maximum size of one write/read segment. If transferred data is bigger, it is split to more segments. Default: ``1E6`` bytes
			- ``OpcTimeout = 10000`` - same as driver.utilities.opc_timeout = 10000. Default: ``30000ms``
			- ``VisaTimeout = 5000`` - same as driver.utilities.visa_timeout = 5000. Default: ``10000ms``
			- ``ViClearExeMode = Disabled`` - viClear() execution mode. Default: ``execute_on_all``
			- ``OpcQueryAfterWrite = True`` - same as driver.utilities.opc_query_after_write = True. Default: ``False``
			- ``StbInErrorCheck = False`` - if true, the driver checks errors with *STB? If false, it uses SYST:ERR?. Default: ``True``
			- ``ScpiQuotes = double'. - for SCPI commands, you can define how strings are quoted. With single or double quotes. Possible values: single | double | {char}. Default: ``single``
			- ``LoggingMode = On`` - Sets the logging status right from the start. Default: ``Off``
			- ``LoggingName = 'MyDevice'`` - Sets the name to represent the session in the log entries. Default: ``'resource_name'``
			- ``LogToGlobalTarget = True`` - Sets the logging target to the class-property previously set with RsSmcv.set_global_logging_target() Default: ``False``
			- ``LoggingToConsole = True`` - Immediately starts logging to the console. Default: False
			- ``LoggingToUdp = True`` - Immediately starts logging to the UDP port. Default: False
			- ``LoggingUdpPort = 49200`` - UDP port to log to. Default: 49200
		:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
		:param id_query: if True, the instrument's model name is verified against the models supported by the driver and eventually throws an exception.
		:param reset: Resets the instrument (sends *RST command) and clears its status sybsystem.
		:param options: string tokens alternating the driver settings.
		:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session."""
		self._core = Core(resource_name, id_query, reset, RsSmcv._driver_options, options, direct_session)
		self._core.driver_version = '5.20.43.0018'
		self._options = options
		self._add_all_global_repcaps()
		self._custom_properties_init()
		self.utilities.default_instrument_setup()
		# noinspection PyTypeChecker
		self._cmd_group = CommandsGroup("ROOT", self._core, None)

	@classmethod
	def from_existing_session(cls, session: object, options: str = None) -> 'RsSmcv':
		"""Creates a new RsSmcv object with the entered 'session' reused. \n
		:param session: can be another driver or a direct pyvisa session.
		:param options: string tokens alternating the driver settings."""
		# noinspection PyTypeChecker
		resource_name = None
		if hasattr(session, 'resource_name'):
			resource_name = getattr(session, 'resource_name')
		return cls(resource_name, False, False, options, session)
		
	@classmethod
	def set_global_logging_target(cls, target) -> None:
		"""Sets global common target stream that each instance can use. To use it, call the following: io.utilities.logger.set_logging_target_global().
		If an instance uses global logging target, it automatically uses the global relative timestamp (if set).
		You can set the target to None to invalidate it."""
		cls._global_logging_target_stream = target

	@classmethod
	def get_global_logging_target(cls):
		"""Returns global common target stream."""
		return cls._global_logging_target_stream

	@classmethod
	def set_global_logging_relative_timestamp(cls, timestamp: datetime) -> None:
		"""Sets global common relative timestamp for log entries. To use it, call the following: io.utilities.logger.set_relative_timestamp_global()"""
		cls._global_logging_relative_timestamp = timestamp

	@classmethod
	def set_global_logging_relative_timestamp_now(cls) -> None:
		"""Sets global common relative timestamp for log entries to this moment.
		To use it, call the following: io.utilities.logger.set_relative_timestamp_global()."""
		cls._global_logging_relative_timestamp = datetime.now()

	@classmethod
	def clear_global_logging_relative_timestamp(cls) -> None:
		"""Clears the global relative timestamp. After this, all the instances using the global relative timestamp continue logging with the absolute timestamps."""
		# noinspection PyTypeChecker
		cls._global_logging_relative_timestamp = None

	@classmethod
	def get_global_logging_relative_timestamp(cls) -> datetime or None:
		"""Returns global common relative timestamp for log entries."""
		return cls._global_logging_relative_timestamp

	def __str__(self) -> str:
		if self._core.io:
			return f"RsSmcv session '{self._core.io.resource_name}'"
		else:
			return f"RsSmcv with session closed"

	def get_total_execution_time(self) -> timedelta:
		"""Returns total time spent by the library on communicating with the instrument.
		This time is always shorter than get_total_time(), since it does not include gaps between the communication.
		You can reset this counter with reset_time_statistics()."""
		return self._core.io.total_execution_time

	def get_total_time(self) -> timedelta:
		"""Returns total time spent by the library on communicating with the instrument.
		This time is always shorter than get_total_time(), since it does not include gaps between the communication.
		You can reset this counter with reset_time_statistics()."""
		return datetime.now() - self._core.io.total_time_startpoint

	def reset_time_statistics(self) -> None:
		"""Resets all execution and total time counters. Affects the results of get_total_time() and get_total_execution_time()"""
		self._core.io.reset_time_statistics()

	@staticmethod
	def assert_minimum_version(min_version: str) -> None:
		"""Asserts that the driver version fulfills the minimum required version you have entered.
		This way you make sure your installed driver is of the entered version or newer."""
		min_version_list = min_version.split('.')
		curr_version_list = '5.20.43.0018'.split('.')
		count_min = len(min_version_list)
		count_curr = len(curr_version_list)
		count = count_min if count_min < count_curr else count_curr
		for i in range(count):
			minimum = int(min_version_list[i])
			curr = int(curr_version_list[i])
			if curr > minimum:
				break
			if curr < minimum:
				raise RsInstrException(f"Assertion for minimum RsSmcv version failed. Current version: '5.20.43.0018', minimum required version: '{min_version}'")

	@staticmethod
	def list_resources(expression: str = '?*::INSTR', visa_select: str = None) -> List[str]:
		"""Finds all the resources defined by the expression
			- '?*' - matches all the available instruments
			- 'USB::?*' - matches all the USB instruments
			- 'TCPIP::192?*' - matches all the LAN instruments with the IP address starting with 192
		:param expression: see the examples in the function
		:param visa_select: optional parameter selecting a specific VISA. Examples: '@ivi', '@rs'
		"""
		rm = VisaSession.get_resource_manager(visa_select)
		resources = rm.list_resources(expression)
		rm.close()
		# noinspection PyTypeChecker
		return resources

	def close(self) -> None:
		"""Closes the active RsSmcv session."""
		self._core.io.close()

	def get_session_handle(self) -> object:
		"""Returns the underlying session handle."""
		return self._core.get_session_handle()

	def _add_all_global_repcaps(self) -> None:
		"""Adds all the repcaps defined as global to the instrument's global repcaps dictionary."""
		self._core.io.add_global_repcap('<HwInstance>', RepeatedCapability("ROOT", 'repcap_hwInstance_get', 'repcap_hwInstance_set', repcap.HwInstance.InstA))

	def repcap_hwInstance_get(self) -> repcap.HwInstance:
		"""Returns Global Repeated capability HwInstance"""
		return self._core.io.get_global_repcap_value('<HwInstance>')

	def repcap_hwInstance_set(self, value: repcap.HwInstance) -> None:
		"""Sets Global Repeated capability HwInstance
		Default value after init: HwInstance.InstA"""
		self._core.io.set_global_repcap_value('<HwInstance>', value)

	def _custom_properties_init(self) -> None:
		"""Adds all the interfaces that are custom for the driver."""
		from .CustomFiles.utilities import Utilities
		self.utilities = Utilities(self._core)
		from .CustomFiles.events import Events
		self.events = Events(self._core)
		from .CustomFiles.arb_files import ArbFiles
		self.arb_files = ArbFiles(self._core)
		from .CustomFiles.digital_modulation import DigitalModulation
		self.digital_modulation = DigitalModulation(self._core)
		
	def _sync_to_custom_properties(self, cloned: 'RsSmcv') -> None:
		"""Synchronises the state of all the custom properties to the entered object."""
		cloned.utilities.sync_from(self.utilities)
		cloned.events.sync_from(self.events)
		cloned.arb_files.sync_from(self.arb_files)
		cloned.digital_modulation.sync_from(self.digital_modulation)

	@property
	def calibration(self):
		"""calibration commands group. 10 Sub-classes, 1 commands."""
		if not hasattr(self, '_calibration'):
			from .Implementations.Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def clock(self):
		"""clock commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_clock'):
			from .Implementations.Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def connector(self):
		"""connector commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_connector'):
			from .Implementations.Connector import ConnectorCls
			self._connector = ConnectorCls(self._core, self._cmd_group)
		return self._connector

	@property
	def device(self):
		"""device commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Implementations.Device import DeviceCls
			self._device = DeviceCls(self._core, self._cmd_group)
		return self._device

	@property
	def diagnostic(self):
		"""diagnostic commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_diagnostic'):
			from .Implementations.Diagnostic import DiagnosticCls
			self._diagnostic = DiagnosticCls(self._core, self._cmd_group)
		return self._diagnostic

	@property
	def display(self):
		"""display commands group. 7 Sub-classes, 3 commands."""
		if not hasattr(self, '_display'):
			from .Implementations.Display import DisplayCls
			self._display = DisplayCls(self._core, self._cmd_group)
		return self._display

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_formatPy'):
			from .Implementations.FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def hardCopy(self):
		"""hardCopy commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_hardCopy'):
			from .Implementations.HardCopy import HardCopyCls
			self._hardCopy = HardCopyCls(self._core, self._cmd_group)
		return self._hardCopy

	@property
	def initiate(self):
		"""initiate commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_initiate'):
			from .Implementations.Initiate import InitiateCls
			self._initiate = InitiateCls(self._core, self._cmd_group)
		return self._initiate

	@property
	def kboard(self):
		"""kboard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kboard'):
			from .Implementations.Kboard import KboardCls
			self._kboard = KboardCls(self._core, self._cmd_group)
		return self._kboard

	@property
	def memory(self):
		"""memory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_memory'):
			from .Implementations.Memory import MemoryCls
			self._memory = MemoryCls(self._core, self._cmd_group)
		return self._memory

	@property
	def massMemory(self):
		"""massMemory commands group. 4 Sub-classes, 9 commands."""
		if not hasattr(self, '_massMemory'):
			from .Implementations.MassMemory import MassMemoryCls
			self._massMemory = MassMemoryCls(self._core, self._cmd_group)
		return self._massMemory

	@property
	def output(self):
		"""output commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_output'):
			from .Implementations.Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def read(self):
		"""read commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_read'):
			from .Implementations.Read import ReadCls
			self._read = ReadCls(self._core, self._cmd_group)
		return self._read

	@property
	def sconfiguration(self):
		"""sconfiguration commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_sconfiguration'):
			from .Implementations.Sconfiguration import SconfigurationCls
			self._sconfiguration = SconfigurationCls(self._core, self._cmd_group)
		return self._sconfiguration

	@property
	def sense(self):
		"""sense commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sense'):
			from .Implementations.Sense import SenseCls
			self._sense = SenseCls(self._core, self._cmd_group)
		return self._sense

	@property
	def slist(self):
		"""slist commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_slist'):
			from .Implementations.Slist import SlistCls
			self._slist = SlistCls(self._core, self._cmd_group)
		return self._slist

	@property
	def source(self):
		"""source commands group. 21 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Implementations.Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	@property
	def status(self):
		"""status commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_status'):
			from .Implementations.Status import StatusCls
			self._status = StatusCls(self._core, self._cmd_group)
		return self._status

	@property
	def system(self):
		"""system commands group. 34 Sub-classes, 28 commands."""
		if not hasattr(self, '_system'):
			from .Implementations.System import SystemCls
			self._system = SystemCls(self._core, self._cmd_group)
		return self._system

	@property
	def test(self):
		"""test commands group. 13 Sub-classes, 4 commands."""
		if not hasattr(self, '_test'):
			from .Implementations.Test import TestCls
			self._test = TestCls(self._core, self._cmd_group)
		return self._test

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Implementations.Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def tsGen(self):
		"""tsGen commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsGen'):
			from .Implementations.TsGen import TsGenCls
			self._tsGen = TsGenCls(self._core, self._cmd_group)
		return self._tsGen

	@property
	def unit(self):
		"""unit commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_unit'):
			from .Implementations.Unit import UnitCls
			self._unit = UnitCls(self._core, self._cmd_group)
		return self._unit

	def get_ffast(self) -> float:
		"""SCPI: FFASt \n
		Snippet: value: float = driver.get_ffast() \n
		No command help available \n
			:return: freq: No help available
		"""
		response = self._core.io.query_str('FFASt?')
		return Conversions.str_to_float(response)

	def set_ffast(self, freq: float) -> None:
		"""SCPI: FFASt \n
		Snippet: driver.set_ffast(freq = 1.0) \n
		No command help available \n
			:param freq: No help available
		"""
		param = Conversions.decimal_value_to_str(freq)
		self._core.io.write(f'FFASt {param}')

	def get_lock(self) -> float:
		"""SCPI: LOCK \n
		Snippet: value: float = driver.get_lock() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('LOCK?')
		return Conversions.str_to_float(response)

	def get_pfast(self) -> float:
		"""SCPI: PFASt \n
		Snippet: value: float = driver.get_pfast() \n
		No command help available \n
			:return: power: No help available
		"""
		response = self._core.io.query_str('PFASt?')
		return Conversions.str_to_float(response)

	def set_pfast(self, power: float) -> None:
		"""SCPI: PFASt \n
		Snippet: driver.set_pfast(power = 1.0) \n
		No command help available \n
			:param power: No help available
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'PFASt {param}')

	def unlock(self, unlock_id: float) -> None:
		"""SCPI: UNLock \n
		Snippet: driver.unlock(unlock_id = 1.0) \n
		No command help available \n
			:param unlock_id: No help available
		"""
		param = Conversions.decimal_value_to_str(unlock_id)
		self._core.io.write(f'UNLock {param}')

	def clone(self) -> 'RsSmcv':
		"""Creates a deep copy of the RsSmcv object. Also copies:
			- All the existing Global repeated capability values
			- All the default group repeated capabilities setting \n
		Does not check the *IDN? response, and does not perform Reset.
		After cloning, you can set all the repeated capabilities settings independentely from the original group.
		Calling close() on the new object does not close the original VISA session"""
		cloned = RsSmcv.from_existing_session(self.get_session_handle(), self._options)
		self._cmd_group.synchronize_repcaps(cloned)
		cloned.repcap_hwInstance_set(self.repcap_hwInstance_get())
		self._sync_to_custom_properties(cloned)
		return cloned

	def restore_all_repcaps_to_default(self) -> None:
		"""Sets all the Group and Global repcaps to their initial values"""
		self._cmd_group.restore_repcaps()
		self.repcap_hwInstance_set(repcap.HwInstance.InstA)
