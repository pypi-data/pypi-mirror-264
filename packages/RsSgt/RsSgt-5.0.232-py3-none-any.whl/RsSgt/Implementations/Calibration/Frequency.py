from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def get_temperature(self) -> str:
		"""SCPI: CALibration:FREQuency:TEMPerature \n
		Snippet: value: str = driver.calibration.frequency.get_temperature() \n
		Queries the delta temperature since the last performed adjustment. \n
			:return: temperature: string
		"""
		response = self._core.io.query_str('CALibration:FREQuency:TEMPerature?')
		return trim_str_response(response)

	def get_measure(self) -> bool:
		"""SCPI: CALibration:FREQuency:[MEASure] \n
		Snippet: value: bool = driver.calibration.frequency.get_measure() \n
		Performs all adjustments which affect the frequency. \n
			:return: synthesis: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('CALibration:FREQuency:MEASure?')
		return Conversions.str_to_bool(response)
