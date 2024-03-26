from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DateCls:
	"""Date commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("date", core, parent)

	def get_local(self) -> str:
		"""SCPI: SYSTem:DATE:LOCal \n
		Snippet: value: str = driver.system.date.get_local() \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:DATE:LOCal?')
		return trim_str_response(response)

	def set_local(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:DATE:LOCal \n
		Snippet: driver.system.date.set_local(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:DATE:LOCal {param}')

	def get_utc(self) -> str:
		"""SCPI: SYSTem:DATE:UTC \n
		Snippet: value: str = driver.system.date.get_utc() \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:DATE:UTC?')
		return trim_str_response(response)

	def set_utc(self, pseudo_string: str) -> None:
		"""SCPI: SYSTem:DATE:UTC \n
		Snippet: driver.system.date.set_utc(pseudo_string = 'abc') \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:DATE:UTC {param}')
