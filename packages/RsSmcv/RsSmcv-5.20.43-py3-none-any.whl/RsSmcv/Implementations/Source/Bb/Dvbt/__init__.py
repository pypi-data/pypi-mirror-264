from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DvbtCls:
	"""Dvbt commands group definition. 51 total commands, 19 Subgroups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dvbt", core, parent)

	@property
	def cell(self):
		"""cell commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cell'):
			from .Cell import CellCls
			self._cell = CellCls(self._core, self._cmd_group)
		return self._cell

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def dvbh(self):
		"""dvbh commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dvbh'):
			from .Dvbh import DvbhCls
			self._dvbh = DvbhCls(self._core, self._cmd_group)
		return self._dvbh

	@property
	def fft(self):
		"""fft commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fft'):
			from .Fft import FftCls
			self._fft = FftCls(self._core, self._cmd_group)
		return self._fft

	@property
	def guard(self):
		"""guard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_guard'):
			from .Guard import GuardCls
			self._guard = GuardCls(self._core, self._cmd_group)
		return self._guard

	@property
	def inputPy(self):
		"""inputPy commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def mpeFec(self):
		"""mpeFec commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mpeFec'):
			from .MpeFec import MpeFecCls
			self._mpeFec = MpeFecCls(self._core, self._cmd_group)
		return self._mpeFec

	@property
	def packetLength(self):
		"""packetLength commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_packetLength'):
			from .PacketLength import PacketLengthCls
			self._packetLength = PacketLengthCls(self._core, self._cmd_group)
		return self._packetLength

	@property
	def prbs(self):
		"""prbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbs'):
			from .Prbs import PrbsCls
			self._prbs = PrbsCls(self._core, self._cmd_group)
		return self._prbs

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rate'):
			from .Rate import RateCls
			self._rate = RateCls(self._core, self._cmd_group)
		return self._rate

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Setting import SettingCls
			self._setting = SettingCls(self._core, self._cmd_group)
		return self._setting

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_source'):
			from .Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	@property
	def stuffing(self):
		"""stuffing commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_stuffing'):
			from .Stuffing import StuffingCls
			self._stuffing = StuffingCls(self._core, self._cmd_group)
		return self._stuffing

	@property
	def testSignal(self):
		"""testSignal commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_testSignal'):
			from .TestSignal import TestSignalCls
			self._testSignal = TestSignalCls(self._core, self._cmd_group)
		return self._testSignal

	@property
	def timeslice(self):
		"""timeslice commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_timeslice'):
			from .Timeslice import TimesliceCls
			self._timeslice = TimesliceCls(self._core, self._cmd_group)
		return self._timeslice

	@property
	def tpsReserved(self):
		"""tpsReserved commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tpsReserved'):
			from .TpsReserved import TpsReservedCls
			self._tpsReserved = TpsReservedCls(self._core, self._cmd_group)
		return self._tpsReserved

	@property
	def used(self):
		"""used commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_used'):
			from .Used import UsedCls
			self._used = UsedCls(self._core, self._cmd_group)
		return self._used

	@property
	def useful(self):
		"""useful commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_useful'):
			from .Useful import UsefulCls
			self._useful = UsefulCls(self._core, self._cmd_group)
		return self._useful

	@property
	def special(self):
		"""special commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_special'):
			from .Special import SpecialCls
			self._special = SpecialCls(self._core, self._cmd_group)
		return self._special

	# noinspection PyTypeChecker
	def get_constel(self) -> enums.DvbtCodingConstel:
		"""SCPI: [SOURce<HW>]:BB:DVBT:CONStel \n
		Snippet: value: enums.DvbtCodingConstel = driver.source.bb.dvbt.get_constel() \n
		Defines the constellation. \n
			:return: constel: T64| T16| T4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:CONStel?')
		return Conversions.str_to_scalar_enum(response, enums.DvbtCodingConstel)

	def set_constel(self, constel: enums.DvbtCodingConstel) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:CONStel \n
		Snippet: driver.source.bb.dvbt.set_constel(constel = enums.DvbtCodingConstel.T16) \n
		Defines the constellation. \n
			:param constel: T64| T16| T4
		"""
		param = Conversions.enum_scalar_to_str(constel, enums.DvbtCodingConstel)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:CONStel {param}')

	def get_dvh_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVBT:DVHState \n
		Snippet: value: bool = driver.source.bb.dvbt.get_dvh_state() \n
		Enables or disables . \n
			:return: dvh_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:DVHState?')
		return Conversions.str_to_bool(response)

	def set_dvh_state(self, dvh_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:DVHState \n
		Snippet: driver.source.bb.dvbt.set_dvh_state(dvh_state = False) \n
		Enables or disables . \n
			:param dvh_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(dvh_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:DVHState {param}')

	# noinspection PyTypeChecker
	def get_hierarchy(self) -> enums.DvbtCodingHierarchy:
		"""SCPI: [SOURce<HW>]:BB:DVBT:HIERarchy \n
		Snippet: value: enums.DvbtCodingHierarchy = driver.source.bb.dvbt.get_hierarchy() \n
		Selects the coding hierarchy. \n
			:return: hierarchy: A4| A2| A1| NONHier
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:HIERarchy?')
		return Conversions.str_to_scalar_enum(response, enums.DvbtCodingHierarchy)

	def set_hierarchy(self, hierarchy: enums.DvbtCodingHierarchy) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:HIERarchy \n
		Snippet: driver.source.bb.dvbt.set_hierarchy(hierarchy = enums.DvbtCodingHierarchy.A1) \n
		Selects the coding hierarchy. \n
			:param hierarchy: A4| A2| A1| NONHier
		"""
		param = Conversions.enum_scalar_to_str(hierarchy, enums.DvbtCodingHierarchy)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:HIERarchy {param}')

	# noinspection PyTypeChecker
	def get_payload(self) -> enums.PayloadTestStuff:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PAYLoad \n
		Snippet: value: enums.PayloadTestStuff = driver.source.bb.dvbt.get_payload() \n
		Defines the payload area content of the packet. \n
			:return: payload: HFF| H00| PRBS
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:PAYLoad?')
		return Conversions.str_to_scalar_enum(response, enums.PayloadTestStuff)

	def set_payload(self, payload: enums.PayloadTestStuff) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PAYLoad \n
		Snippet: driver.source.bb.dvbt.set_payload(payload = enums.PayloadTestStuff.H00) \n
		Defines the payload area content of the packet. \n
			:param payload: HFF| H00| PRBS
		"""
		param = Conversions.enum_scalar_to_str(payload, enums.PayloadTestStuff)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:PAYLoad {param}')

	def get_pid(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PID \n
		Snippet: value: int = driver.source.bb.dvbt.get_pid() \n
		Sets the . \n
			:return: pid: integer Range: #H0000 to #H1FFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:PID?')
		return Conversions.str_to_int(response)

	def set_pid(self, pid: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PID \n
		Snippet: driver.source.bb.dvbt.set_pid(pid = 1) \n
		Sets the . \n
			:param pid: integer Range: #H0000 to #H1FFF
		"""
		param = Conversions.decimal_value_to_str(pid)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:PID {param}')

	# noinspection PyTypeChecker
	def get_pid_test_pack(self) -> enums.PidTestPacket:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PIDTestpack \n
		Snippet: value: enums.PidTestPacket = driver.source.bb.dvbt.get_pid_test_pack() \n
		If a header is present in the test packet ('Test TS Packet > Head/184 Payload') , you can specify a fixed or variable
		packet identifier (PID) . \n
			:return: pid_test_packet: NULL| VARiable
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:PIDTestpack?')
		return Conversions.str_to_scalar_enum(response, enums.PidTestPacket)

	def set_pid_test_pack(self, pid_test_packet: enums.PidTestPacket) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PIDTestpack \n
		Snippet: driver.source.bb.dvbt.set_pid_test_pack(pid_test_packet = enums.PidTestPacket.NULL) \n
		If a header is present in the test packet ('Test TS Packet > Head/184 Payload') , you can specify a fixed or variable
		packet identifier (PID) . \n
			:param pid_test_packet: NULL| VARiable
		"""
		param = Conversions.enum_scalar_to_str(pid_test_packet, enums.PidTestPacket)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:PIDTestpack {param}')

	def preset(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PRESet \n
		Snippet: driver.source.bb.dvbt.preset() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:DVBT:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:PRESet \n
		Snippet: driver.source.bb.dvbt.preset_with_opc() \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:DVBT:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmcv.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DVBT:PRESet', opc_timeout_ms)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVBT:STATe \n
		Snippet: value: bool = driver.source.bb.dvbt.get_state() \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:STATe \n
		Snippet: driver.source.bb.dvbt.set_state(state = False) \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:STATe {param}')

	# noinspection PyTypeChecker
	def get_ts_packet(self) -> enums.SettingsTestTsPacket:
		"""SCPI: [SOURce<HW>]:BB:DVBT:TSPacket \n
		Snippet: value: enums.SettingsTestTsPacket = driver.source.bb.dvbt.get_ts_packet() \n
		Specifies the structure of the test transport stream packet that is fed to the modulator. \n
			:return: ts_packet: S187| H184
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVBT:TSPacket?')
		return Conversions.str_to_scalar_enum(response, enums.SettingsTestTsPacket)

	def set_ts_packet(self, ts_packet: enums.SettingsTestTsPacket) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVBT:TSPacket \n
		Snippet: driver.source.bb.dvbt.set_ts_packet(ts_packet = enums.SettingsTestTsPacket.H184) \n
		Specifies the structure of the test transport stream packet that is fed to the modulator. \n
			:param ts_packet: S187| H184
		"""
		param = Conversions.enum_scalar_to_str(ts_packet, enums.SettingsTestTsPacket)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVBT:TSPacket {param}')

	def clone(self) -> 'DvbtCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DvbtCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
