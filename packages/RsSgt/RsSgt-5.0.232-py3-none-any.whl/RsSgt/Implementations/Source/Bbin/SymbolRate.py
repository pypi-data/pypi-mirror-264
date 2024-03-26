from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRateCls:
	"""SymbolRate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("symbolRate", core, parent)

	def get_actual(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:SRATe:[ACTual] \n
		Snippet: value: float = driver.source.bbin.symbolRate.get_actual() \n
		Sets the sample rate of the external digital baseband signal. \n
			:return: actual: float Range: 25E6 to 250E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:SRATe:ACTual?')
		return Conversions.str_to_float(response)

	def set_actual(self, actual: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:SRATe:[ACTual] \n
		Snippet: driver.source.bbin.symbolRate.set_actual(actual = 1.0) \n
		Sets the sample rate of the external digital baseband signal. \n
			:param actual: float Range: 25E6 to 250E6
		"""
		param = Conversions.decimal_value_to_str(actual)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:SRATe:ACTual {param}')
