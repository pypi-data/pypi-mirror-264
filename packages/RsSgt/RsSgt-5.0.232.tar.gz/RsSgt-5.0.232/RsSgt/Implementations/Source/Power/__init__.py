from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 24 total commands, 6 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def alc(self):
		"""alc commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_alc'):
			from .Alc import AlcCls
			self._alc = AlcCls(self._core, self._cmd_group)
		return self._alc

	@property
	def attenuation(self):
		"""attenuation commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_attenuation'):
			from .Attenuation import AttenuationCls
			self._attenuation = AttenuationCls(self._core, self._cmd_group)
		return self._attenuation

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_range'):
			from .Range import RangeCls
			self._range = RangeCls(self._core, self._cmd_group)
		return self._range

	@property
	def servoing(self):
		"""servoing commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_servoing'):
			from .Servoing import ServoingCls
			self._servoing = ServoingCls(self._core, self._cmd_group)
		return self._servoing

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	# noinspection PyTypeChecker
	def get_lmode(self) -> enums.PowLevMode:
		"""SCPI: [SOURce<HW>]:POWer:LMODe \n
		Snippet: value: enums.PowLevMode = driver.source.power.get_lmode() \n
		Selects the level mode. \n
			:return: lev_mode: NORMal| LOWNoise| LOWDistortion NORM automatic selection of the best settings LNOISe settings for lowest noise LDIStortion settings for lowest distortions
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LMODe?')
		return Conversions.str_to_scalar_enum(response, enums.PowLevMode)

	def set_lmode(self, lev_mode: enums.PowLevMode) -> None:
		"""SCPI: [SOURce<HW>]:POWer:LMODe \n
		Snippet: driver.source.power.set_lmode(lev_mode = enums.PowLevMode.LOWDistortion) \n
		Selects the level mode. \n
			:param lev_mode: NORMal| LOWNoise| LOWDistortion NORM automatic selection of the best settings LNOISe settings for lowest noise LDIStortion settings for lowest distortions
		"""
		param = Conversions.enum_scalar_to_str(lev_mode, enums.PowLevMode)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LMODe {param}')

	def get_pep(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:PEP \n
		Snippet: value: float = driver.source.power.get_pep() \n
		Queries the RF signal peak envelope power. \n
			:return: pep: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:PEP?')
		return Conversions.str_to_float(response)

	def get_power(self) -> float:
		"""SCPI: [SOURce<HW>]:POWer:POWer \n
		Snippet: value: float = driver.source.power.get_power() \n
		Sets the level at the RF output connector. This value does not consider a specified offset.
		The command [:SOURce]:POWer[:LEVel][:IMMediate][:AMPLitude] sets the level of the 'Level' display, that means the level
		containing offset. \n
			:return: amplitude: float Range: -20 to 25
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:POWer?')
		return Conversions.str_to_float(response)

	def set_power(self, amplitude: float) -> None:
		"""SCPI: [SOURce<HW>]:POWer:POWer \n
		Snippet: driver.source.power.set_power(amplitude = 1.0) \n
		Sets the level at the RF output connector. This value does not consider a specified offset.
		The command [:SOURce]:POWer[:LEVel][:IMMediate][:AMPLitude] sets the level of the 'Level' display, that means the level
		containing offset. \n
			:param amplitude: float Range: -20 to 25
		"""
		param = Conversions.decimal_value_to_str(amplitude)
		self._core.io.write(f'SOURce<HwInstance>:POWer:POWer {param}')

	# noinspection PyTypeChecker
	def get_scharacteristic(self) -> enums.PowLevBehaviour:
		"""SCPI: [SOURce<HW>]:POWer:SCHaracteristic \n
		Snippet: value: enums.PowLevBehaviour = driver.source.power.get_scharacteristic() \n
		Selects the characteristic for the level setting. \n
			:return: characteristic: AUTO| UNINterrupted| CVSWr| USER| MONotone UNINterrupted uninterrupted level setting CVSWr constant-VSWR MONotone strictly monotone
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:SCHaracteristic?')
		return Conversions.str_to_scalar_enum(response, enums.PowLevBehaviour)

	def set_scharacteristic(self, characteristic: enums.PowLevBehaviour) -> None:
		"""SCPI: [SOURce<HW>]:POWer:SCHaracteristic \n
		Snippet: driver.source.power.set_scharacteristic(characteristic = enums.PowLevBehaviour.AUTO) \n
		Selects the characteristic for the level setting. \n
			:param characteristic: AUTO| UNINterrupted| CVSWr| USER| MONotone UNINterrupted uninterrupted level setting CVSWr constant-VSWR MONotone strictly monotone
		"""
		param = Conversions.enum_scalar_to_str(characteristic, enums.PowLevBehaviour)
		self._core.io.write(f'SOURce<HwInstance>:POWer:SCHaracteristic {param}')

	def clone(self) -> 'PowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
