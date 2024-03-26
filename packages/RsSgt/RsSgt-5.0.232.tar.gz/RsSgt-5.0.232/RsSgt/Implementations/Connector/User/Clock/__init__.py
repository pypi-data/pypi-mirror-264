from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ClockCls:
	"""Clock commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("clock", core, parent)

	@property
	def impedance(self):
		"""impedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_impedance'):
			from .Impedance import ImpedanceCls
			self._impedance = ImpedanceCls(self._core, self._cmd_group)
		return self._impedance

	@property
	def slope(self):
		"""slope commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slope'):
			from .Slope import SlopeCls
			self._slope = SlopeCls(self._core, self._cmd_group)
		return self._slope

	def clone(self) -> 'ClockCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ClockCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
