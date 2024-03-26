from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SystemCls:
	"""System commands group definition. 43 total commands, 8 Subgroups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("system", core, parent)

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_date'):
			from .Date import DateCls
			self._date = DateCls(self._core, self._cmd_group)
		return self._date

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Device import DeviceCls
			self._device = DeviceCls(self._core, self._cmd_group)
		return self._device

	@property
	def deviceFootprint(self):
		"""deviceFootprint commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_deviceFootprint'):
			from .DeviceFootprint import DeviceFootprintCls
			self._deviceFootprint = DeviceFootprintCls(self._core, self._cmd_group)
		return self._deviceFootprint

	@property
	def error(self):
		"""error commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_error'):
			from .Error import ErrorCls
			self._error = ErrorCls(self._core, self._cmd_group)
		return self._error

	@property
	def fpreset(self):
		"""fpreset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fpreset'):
			from .Fpreset import FpresetCls
			self._fpreset = FpresetCls(self._core, self._cmd_group)
		return self._fpreset

	@property
	def help(self):
		"""help commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_help'):
			from .Help import HelpCls
			self._help = HelpCls(self._core, self._cmd_group)
		return self._help

	@property
	def lock(self):
		"""lock commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_lock'):
			from .Lock import LockCls
			self._lock = LockCls(self._core, self._cmd_group)
		return self._lock

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	def get_did(self) -> str:
		"""SCPI: SYSTem:DID \n
		Snippet: value: str = driver.system.get_did() \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:DID?')
		return trim_str_response(response)

	def preset(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:PRESet \n
		Snippet: driver.system.preset(pseudo_string = 'abc') \n
			INTRO_CMD_HELP: Triggers an instrument reset. It has the same effect as: \n
			- The *RST command
			- The 'SGMA-GUI > Instrument Name > Preset' function. However, the command does not close open GUI dialogs like the function does. \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:PRESet {param}')

	def preset_all(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:PRESet:ALL \n
		Snippet: driver.system.preset_all(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:PRESet:ALL {param}')

	def preset_base(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:PRESet:BASE \n
		Snippet: driver.system.preset_base(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:PRESet:BASE {param}')

	def reset(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:RESet \n
		Snippet: driver.system.reset(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:RESet {param}')

	def reset_all(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:RESet:ALL \n
		Snippet: driver.system.reset_all(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:RESet:ALL {param}')

	def reset_base(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:RESet:BASE \n
		Snippet: driver.system.reset_base(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:RESet:BASE {param}')

	def set_srestore(self, data_set: int) -> None:
		"""SCPI: SYSTem:SREStore \n
		Snippet: driver.system.set_srestore(data_set = 1) \n
		No command help available \n
			:param data_set: No help available
		"""
		param = Conversions.decimal_value_to_str(data_set)
		self._core.io.write(f'SYSTem:SREStore {param}')

	def set_ssave(self, data_set: int) -> None:
		"""SCPI: SYSTem:SSAVe \n
		Snippet: driver.system.set_ssave(data_set = 1) \n
		No command help available \n
			:param data_set: No help available
		"""
		param = Conversions.decimal_value_to_str(data_set)
		self._core.io.write(f'SYSTem:SSAVe {param}')

	def get_tzone(self) -> str:
		"""SCPI: SYSTem:TZONe \n
		Snippet: value: str = driver.system.get_tzone() \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TZONe?')
		return trim_str_response(response)

	def set_tzone(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:TZONe \n
		Snippet: driver.system.set_tzone(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TZONe {param}')

	def get_version(self) -> str:
		"""SCPI: SYSTem:VERSion \n
		Snippet: value: str = driver.system.get_version() \n
		Queries the SCPI version the instrument's command set complies with. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SYSTem:VERSion?')
		return trim_str_response(response)

	def clone(self) -> 'SystemCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SystemCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
