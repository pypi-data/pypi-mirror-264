from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LimitCls:
	"""Limit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limit", core, parent)

	def get_amplitude(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:LIMit:[AMPLitude] \n
		Snippet: value: float = driver.source.power.limit.get_amplitude() \n
		Sets the upper limit of the RF signal power. An instrument preset does not affect this value. A factory preset (method
		RsSgt.System.Fpreset.set) sets the specified factory upper limit value. \n
			:return: amplitude: float Range: -120 to 25
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LIMit:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, amplitude: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:LIMit:[AMPLitude] \n
		Snippet: driver.source.power.limit.set_amplitude(amplitude = 1.0) \n
		Sets the upper limit of the RF signal power. An instrument preset does not affect this value. A factory preset (method
		RsSgt.System.Fpreset.set) sets the specified factory upper limit value. \n
			:param amplitude: float Range: -120 to 25
		"""
		param = Conversions.decimal_value_to_str(amplitude)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LIMit:AMPLitude {param}')
