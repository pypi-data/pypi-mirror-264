from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 64 total commands, 9 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def bb(self):
		"""bb commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_bb'):
			from .Bb import BbCls
			self._bb = BbCls(self._core, self._cmd_group)
		return self._bb

	@property
	def bbin(self):
		"""bbin commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbin'):
			from .Bbin import BbinCls
			self._bbin = BbinCls(self._core, self._cmd_group)
		return self._bbin

	@property
	def frequency(self):
		"""frequency commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def inputPy(self):
		"""inputPy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def iq(self):
		"""iq commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	@property
	def loscillator(self):
		"""loscillator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_loscillator'):
			from .Loscillator import LoscillatorCls
			self._loscillator = LoscillatorCls(self._core, self._cmd_group)
		return self._loscillator

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def power(self):
		"""power commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def roscillator(self):
		"""roscillator commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_roscillator'):
			from .Roscillator import RoscillatorCls
			self._roscillator = RoscillatorCls(self._core, self._cmd_group)
		return self._roscillator

	# noinspection PyTypeChecker
	def get_op_mode(self) -> enums.OpMode:
		"""SCPI: [SOURce<HW>]:OPMode \n
		Snippet: value: enums.OpMode = driver.source.get_op_mode() \n
		Sets the operation mode. \n
			:return: op_mode: NORMal| BBBYpass NORMal normal operation BBBYpass Baseband bypass mode
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:OPMode?')
		return Conversions.str_to_scalar_enum(response, enums.OpMode)

	def set_op_mode(self, op_mode: enums.OpMode) -> None:
		"""SCPI: [SOURce<HW>]:OPMode \n
		Snippet: driver.source.set_op_mode(op_mode = enums.OpMode.BBBYpass) \n
		Sets the operation mode. \n
			:param op_mode: NORMal| BBBYpass NORMal normal operation BBBYpass Baseband bypass mode
		"""
		param = Conversions.enum_scalar_to_str(op_mode, enums.OpMode)
		self._core.io.write(f'SOURce<HwInstance>:OPMode {param}')

	def clone(self) -> 'SourceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SourceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
