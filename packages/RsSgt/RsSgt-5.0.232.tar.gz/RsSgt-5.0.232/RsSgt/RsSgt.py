from typing import ClassVar, List

from .Internal.Core import Core
from .Internal.InstrumentErrors import RsInstrException
from .Internal.CommandsGroup import CommandsGroup
from .Internal.VisaSession import VisaSession
from datetime import datetime, timedelta
from .Internal import Conversions
from .Internal.StructBase import StructBase
from .Internal.ArgStruct import ArgStruct
from . import repcap
from .Internal.RepeatedCapability import RepeatedCapability


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsSgt:
	"""176 total commands, 10 Subgroups, 4 group commands"""
	_driver_options = "SupportedInstrModels = SMW/SMBV/SGT/SMA/SMM/SMCV, SupportedIdnPatterns = SMW/SMBV/SGT/SMA/SMM/SMCV, SimulationIdnString = 'Rohde&Schwarz,SGT100A,100001,5.0.232.0031'"
	_global_logging_relative_timestamp: ClassVar[datetime] = None
	_global_logging_target_stream: ClassVar = None

	def __init__(self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
		"""Initializes new RsSgt session. \n
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
			- ``LogToGlobalTarget = True`` - Sets the logging target to the class-property previously set with RsSgt.set_global_logging_target() Default: ``False``
			- ``LoggingToConsole = True`` - Immediately starts logging to the console. Default: False
			- ``LoggingToUdp = True`` - Immediately starts logging to the UDP port. Default: False
			- ``LoggingUdpPort = 49200`` - UDP port to log to. Default: 49200
		:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
		:param id_query: if True, the instrument's model name is verified against the models supported by the driver and eventually throws an exception.
		:param reset: Resets the instrument (sends *RST command) and clears its status sybsystem.
		:param options: string tokens alternating the driver settings.
		:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session."""
		self._core = Core(resource_name, id_query, reset, RsSgt._driver_options, options, direct_session)
		self._core.driver_version = '5.0.232.0031'
		self._options = options
		self._add_all_global_repcaps()
		self._custom_properties_init()
		self.utilities.default_instrument_setup()
		# noinspection PyTypeChecker
		self._cmd_group = CommandsGroup("ROOT", self._core, None)

	@classmethod
	def from_existing_session(cls, session: object, options: str = None) -> 'RsSgt':
		"""Creates a new RsSgt object with the entered 'session' reused. \n
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
			return f"RsSgt session '{self._core.io.resource_name}'"
		else:
			return f"RsSgt with session closed"

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
		curr_version_list = '5.0.232.0031'.split('.')
		count_min = len(min_version_list)
		count_curr = len(curr_version_list)
		count = count_min if count_min < count_curr else count_curr
		for i in range(count):
			minimum = int(min_version_list[i])
			curr = int(curr_version_list[i])
			if curr > minimum:
				break
			if curr < minimum:
				raise RsInstrException(f"Assertion for minimum RsSgt version failed. Current version: '5.0.232.0031', minimum required version: '{min_version}'")

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
		"""Closes the active RsSgt session."""
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
		
	def _sync_to_custom_properties(self, cloned: 'RsSgt') -> None:
		"""Synchronises the state of all the custom properties to the entered object."""
		cloned.utilities.sync_from(self.utilities)
		cloned.events.sync_from(self.events)
		cloned.arb_files.sync_from(self.arb_files)
		cloned.digital_modulation.sync_from(self.digital_modulation)

	@property
	def calibration(self):
		"""calibration commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_calibration'):
			from .Implementations.Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def connector(self):
		"""connector commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_connector'):
			from .Implementations.Connector import ConnectorCls
			self._connector = ConnectorCls(self._core, self._cmd_group)
		return self._connector

	@property
	def diagnostic(self):
		"""diagnostic commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_diagnostic'):
			from .Implementations.Diagnostic import DiagnosticCls
			self._diagnostic = DiagnosticCls(self._core, self._cmd_group)
		return self._diagnostic

	@property
	def massMemory(self):
		"""massMemory commands group. 4 Sub-classes, 9 commands."""
		if not hasattr(self, '_massMemory'):
			from .Implementations.MassMemory import MassMemoryCls
			self._massMemory = MassMemoryCls(self._core, self._cmd_group)
		return self._massMemory

	@property
	def output(self):
		"""output commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Implementations.Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def sconfiguration(self):
		"""sconfiguration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sconfiguration'):
			from .Implementations.Sconfiguration import SconfigurationCls
			self._sconfiguration = SconfigurationCls(self._core, self._cmd_group)
		return self._sconfiguration

	@property
	def status(self):
		"""status commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_status'):
			from .Implementations.Status import StatusCls
			self._status = StatusCls(self._core, self._cmd_group)
		return self._status

	@property
	def system(self):
		"""system commands group. 8 Sub-classes, 11 commands."""
		if not hasattr(self, '_system'):
			from .Implementations.System import SystemCls
			self._system = SystemCls(self._core, self._cmd_group)
		return self._system

	@property
	def test(self):
		"""test commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_test'):
			from .Implementations.Test import TestCls
			self._test = TestCls(self._core, self._cmd_group)
		return self._test

	@property
	def source(self):
		"""source commands group. 9 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Implementations.Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	def get_ffast(self) -> float:
		"""SCPI: FFASt \n
		Snippet: value: float = driver.get_ffast() \n
		Special command to set the RF output frequency with minimum latency. No unit (e.g. Hz) allowed. Bypasses the status
		system so command *OPC? cannot be appended. \n
			:return: freq: float
		"""
		response = self._core.io.query_str('FFASt?')
		return Conversions.str_to_float(response)

	def set_ffast(self, freq: float) -> None:
		"""SCPI: FFASt \n
		Snippet: driver.set_ffast(freq = 1.0) \n
		Special command to set the RF output frequency with minimum latency. No unit (e.g. Hz) allowed. Bypasses the status
		system so command *OPC? cannot be appended. \n
			:param freq: float
		"""
		param = Conversions.decimal_value_to_str(freq)
		self._core.io.write(f'FFASt {param}')

	# noinspection PyTypeChecker
	class LockStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Lock_Request_Id: float: Number 0 test query to prove whether the instrument is locked Controller ID request lock from the controller with the specified Controller ID
			- Value: float: Number 0 request refused; the instrument is already locked to other Lock Request Id, i.e. to another controller 1 request granted"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lock_Request_Id'),
			ArgStruct.scalar_float('Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lock_Request_Id: float = None
			self.Value: float = None

	def get_lock(self) -> LockStruct:
		"""SCPI: LOCK \n
		Snippet: value: LockStruct = driver.get_lock() \n
		Sends a lock request ID which uniquely identifies the controller to the instrument. \n
			:return: structure: for return value, see the help for LockStruct structure arguments.
		"""
		return self._core.io.query_struct('LOCK?', self.__class__.LockStruct())

	def get_pfast(self) -> float:
		"""SCPI: PFASt \n
		Snippet: value: float = driver.get_pfast() \n
		Special command to set the RF output level with minimum latency at the RF output connector. This value does not consider
		a specified offset. No unit (e.g. dBm) allowed. Bypasses the status system so command *OPC? cannot be appended. \n
			:return: power: float
		"""
		response = self._core.io.query_str('PFASt?')
		return Conversions.str_to_float(response)

	def set_pfast(self, power: float) -> None:
		"""SCPI: PFASt \n
		Snippet: driver.set_pfast(power = 1.0) \n
		Special command to set the RF output level with minimum latency at the RF output connector. This value does not consider
		a specified offset. No unit (e.g. dBm) allowed. Bypasses the status system so command *OPC? cannot be appended. \n
			:param power: float
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'PFASt {param}')

	def unlock(self, unlock_id: float) -> None:
		"""SCPI: UNLock \n
		Snippet: driver.unlock(unlock_id = 1.0) \n
		Unlocks an instrument locked to a controller with Controller ID = <Unlock Id>. \n
			:param unlock_id: Number Unlock ID which uniquely identifies the controller to the instrument. The value must match the Controller ID Lock Request Id set with the command [CMDLINKRESOLVED #Lock CMDLINKRESOLVED]. 0 Clear lock regardless of locking state
		"""
		param = Conversions.decimal_value_to_str(unlock_id)
		self._core.io.write(f'UNLock {param}')

	def clone(self) -> 'RsSgt':
		"""Creates a deep copy of the RsSgt object. Also copies:
			- All the existing Global repeated capability values
			- All the default group repeated capabilities setting \n
		Does not check the *IDN? response, and does not perform Reset.
		After cloning, you can set all the repeated capabilities settings independentely from the original group.
		Calling close() on the new object does not close the original VISA session"""
		cloned = RsSgt.from_existing_session(self.get_session_handle(), self._options)
		self._cmd_group.synchronize_repcaps(cloned)
		cloned.repcap_hwInstance_set(self.repcap_hwInstance_get())
		self._sync_to_custom_properties(cloned)
		return cloned

	def restore_all_repcaps_to_default(self) -> None:
		"""Sets all the Group and Global repcaps to their initial values"""
		self._cmd_group.restore_repcaps()
		self.repcap_hwInstance_set(repcap.HwInstance.InstA)
