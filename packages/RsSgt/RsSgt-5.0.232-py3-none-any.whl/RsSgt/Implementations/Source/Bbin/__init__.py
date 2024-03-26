from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbinCls:
	"""Bbin commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bbin", core, parent)

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	def get_odelay(self) -> float:
		"""SCPI: [SOURce<HW>]:BBIN:ODELay \n
		Snippet: value: float = driver.source.bbin.get_odelay() \n
		Seds the output delay of the external baseband signal. \n
			:return: delay: float Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:ODELay?')
		return Conversions.str_to_float(response)

	def set_odelay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:ODELay \n
		Snippet: driver.source.bbin.set_odelay(delay = 1.0) \n
		Seds the output delay of the external baseband signal. \n
			:param delay: float Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:ODELay {param}')

	def clone(self) -> 'BbinCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbinCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
