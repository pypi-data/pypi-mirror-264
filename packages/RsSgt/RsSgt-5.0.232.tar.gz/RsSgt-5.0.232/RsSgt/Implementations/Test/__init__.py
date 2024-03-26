from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TestCls:
	"""Test commands group definition. 3 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("test", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def keyboard(self):
		"""keyboard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_keyboard'):
			from .Keyboard import KeyboardCls
			self._keyboard = KeyboardCls(self._core, self._cmd_group)
		return self._keyboard

	def clone(self) -> 'TestCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TestCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
