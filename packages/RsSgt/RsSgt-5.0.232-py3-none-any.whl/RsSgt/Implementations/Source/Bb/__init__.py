from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbCls:
	"""Bb commands group definition. 8 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bb", core, parent)

	@property
	def impairment(self):
		"""impairment commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_impairment'):
			from .Impairment import ImpairmentCls
			self._impairment = ImpairmentCls(self._core, self._cmd_group)
		return self._impairment

	def get_foffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: value: float = driver.source.bb.get_foffset() \n
		Sets the frequency offset for the baseband signal. The offset affects the signal on the baseband block output. It shifts
		the useful baseband signal in the center frequency. \n
			:return: foffset: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, foffset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:FOFFset \n
		Snippet: driver.source.bb.set_foffset(foffset = 1.0) \n
		Sets the frequency offset for the baseband signal. The offset affects the signal on the baseband block output. It shifts
		the useful baseband signal in the center frequency. \n
			:param foffset: float
		"""
		param = Conversions.decimal_value_to_str(foffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:FOFFset {param}')

	def get_poffset(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: value: float = driver.source.bb.get_poffset() \n
		Sets the relative phase offset of the baseband signal. The phase offset affects the signal of the 'Baseband Block' output. \n
			:return: ph_offset: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, ph_offset: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:POFFset \n
		Snippet: driver.source.bb.set_poffset(ph_offset = 1.0) \n
		Sets the relative phase offset of the baseband signal. The phase offset affects the signal of the 'Baseband Block' output. \n
			:param ph_offset: float
		"""
		param = Conversions.decimal_value_to_str(ph_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:POFFset {param}')

	def clone(self) -> 'BbCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
