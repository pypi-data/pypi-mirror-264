from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RadarCls:
	"""Radar commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("radar", core, parent)

	@property
	def base(self):
		"""base commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_base'):
			from .Base import BaseCls
			self._base = BaseCls(self._core, self._cmd_group)
		return self._base

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	def get_lsensitivity(self) -> bool:
		"""SCPI: [SOURce<HW>]:AREGenerator:RADar:LSENsitivity \n
		Snippet: value: bool = driver.source.areGenerator.radar.get_lsensitivity() \n
		Defines if low sensitivity is used or not. \n
			:return: areg_radar_low_sen: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:RADar:LSENsitivity?')
		return Conversions.str_to_bool(response)

	def set_lsensitivity(self, areg_radar_low_sen: bool) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:RADar:LSENsitivity \n
		Snippet: driver.source.areGenerator.radar.set_lsensitivity(areg_radar_low_sen = False) \n
		Defines if low sensitivity is used or not. \n
			:param areg_radar_low_sen: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(areg_radar_low_sen)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:RADar:LSENsitivity {param}')

	def clone(self) -> 'RadarCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RadarCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
