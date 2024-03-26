from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BaseCls:
	"""Base commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("base", core, parent)

	def get_attenuation(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:RADar:BASE:ATTenuation \n
		Snippet: value: int = driver.source.areGenerator.radar.base.get_attenuation() \n
		No command help available \n
			:return: areg_base_att: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:RADar:BASE:ATTenuation?')
		return Conversions.str_to_int(response)

	def set_attenuation(self, areg_base_att: int) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:RADar:BASE:ATTenuation \n
		Snippet: driver.source.areGenerator.radar.base.set_attenuation(areg_base_att = 1) \n
		No command help available \n
			:param areg_base_att: No help available
		"""
		param = Conversions.decimal_value_to_str(areg_base_att)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:RADar:BASE:ATTenuation {param}')
