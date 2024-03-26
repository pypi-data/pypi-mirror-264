from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 8 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def daylightSavingTime(self):
		"""daylightSavingTime commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_daylightSavingTime'):
			from .DaylightSavingTime import DaylightSavingTimeCls
			self._daylightSavingTime = DaylightSavingTimeCls(self._core, self._cmd_group)
		return self._daylightSavingTime

	@property
	def hrTimer(self):
		"""hrTimer commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_hrTimer'):
			from .HrTimer import HrTimerCls
			self._hrTimer = HrTimerCls(self._core, self._cmd_group)
		return self._hrTimer

	def get_local(self) -> str:
		"""SCPI: SYSTem:TIME:LOCal \n
		Snippet: value: str = driver.system.time.get_local() \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:LOCal?')
		return trim_str_response(response)

	def set_local(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:TIME:LOCal \n
		Snippet: driver.system.time.set_local(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:LOCal {param}')

	def get_utc(self) -> str:
		"""SCPI: SYSTem:TIME:UTC \n
		Snippet: value: str = driver.system.time.get_utc() \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:UTC?')
		return trim_str_response(response)

	def set_utc(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:TIME:UTC \n
		Snippet: driver.system.time.set_utc(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:UTC {param}')

	def clone(self) -> 'TimeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TimeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
