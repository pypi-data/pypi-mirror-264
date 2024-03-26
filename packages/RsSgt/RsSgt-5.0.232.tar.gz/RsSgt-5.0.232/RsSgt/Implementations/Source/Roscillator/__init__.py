from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RoscillatorCls:
	"""Roscillator commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("roscillator", core, parent)

	@property
	def external(self):
		"""external commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SourceInt:
		"""SCPI: [SOURce<HW>]:ROSCillator:SOURce \n
		Snippet: value: enums.SourceInt = driver.source.roscillator.get_source() \n
		Select the reference oscillator signal source. \n
			:return: source: INTernal| EXTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ROSCillator:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_source(self, source: enums.SourceInt) -> None:
		"""SCPI: [SOURce<HW>]:ROSCillator:SOURce \n
		Snippet: driver.source.roscillator.set_source(source = enums.SourceInt.EXTernal) \n
		Select the reference oscillator signal source. \n
			:param source: INTernal| EXTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SourceInt)
		self._core.io.write(f'SOURce<HwInstance>:ROSCillator:SOURce {param}')

	def clone(self) -> 'RoscillatorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RoscillatorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
