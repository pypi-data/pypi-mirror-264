from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	# noinspection PyTypeChecker
	def get_frequency(self) -> enums.RoscFreqExt:
		"""SCPI: [SOURce<HW>]:ROSCillator:EXTernal:FREQuency \n
		Snippet: value: enums.RoscFreqExt = driver.source.roscillator.external.get_frequency() \n
		Selects the frequency of the external reference. \n
			:return: ext_freq: 10MHZ| 100MHZ| 1000MHZ| 13MHZ 13MHZ requires RF board with part number 1419.5308.02. To find out the RF board installed in the instrument: Select 'SGMA-GUI instrument name Setup Hardware Config' 'RF Assembly' Observe the part number of the assembly 'RfBoard'.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ROSCillator:EXTernal:FREQuency?')
		return Conversions.str_to_scalar_enum(response, enums.RoscFreqExt)

	def set_frequency(self, ext_freq: enums.RoscFreqExt) -> None:
		"""SCPI: [SOURce<HW>]:ROSCillator:EXTernal:FREQuency \n
		Snippet: driver.source.roscillator.external.set_frequency(ext_freq = enums.RoscFreqExt._1000MHZ) \n
		Selects the frequency of the external reference. \n
			:param ext_freq: 10MHZ| 100MHZ| 1000MHZ| 13MHZ 13MHZ requires RF board with part number 1419.5308.02. To find out the RF board installed in the instrument: Select 'SGMA-GUI instrument name Setup Hardware Config' 'RF Assembly' Observe the part number of the assembly 'RfBoard'.
		"""
		param = Conversions.enum_scalar_to_str(ext_freq, enums.RoscFreqExt)
		self._core.io.write(f'SOURce<HwInstance>:ROSCillator:EXTernal:FREQuency {param}')
