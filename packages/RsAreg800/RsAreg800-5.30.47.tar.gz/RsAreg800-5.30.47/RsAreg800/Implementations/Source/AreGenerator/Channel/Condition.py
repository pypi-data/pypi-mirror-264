from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConditionCls:
	"""Condition commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("condition", core, parent)

	def get_info(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:CONDition:INFO \n
		Snippet: value: str = driver.source.areGenerator.channel.condition.get_info() \n
		Displays a status message for the input power for the related radar channel. \n
			:return: areg_pow_led_info: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:CONDition:INFO?')
		return trim_str_response(response)

	def set_info(self, areg_pow_led_info: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:CONDition:INFO \n
		Snippet: driver.source.areGenerator.channel.condition.set_info(areg_pow_led_info = 'abc') \n
		Displays a status message for the input power for the related radar channel. \n
			:param areg_pow_led_info: string
		"""
		param = Conversions.value_to_quoted_str(areg_pow_led_info)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:CONDition:INFO {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.AregPlEd:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:CONDition \n
		Snippet: value: enums.AregPlEd = driver.source.areGenerator.channel.condition.get_value() \n
		Displays the status of the power LED for the related radar channel. \n
			:return: areg_pow_led_statu: INACtive| WARNing| ERRor| OK INACtive The channel is inactive. The power LED lights grey. WARNing Displays a warning for the channel. The power LED lights yellow. ERRor Displays an error for the channel. The power LED lights red. OK The channel is active and works properly. The power LED lights green.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:CONDition?')
		return Conversions.str_to_scalar_enum(response, enums.AregPlEd)

	def set_value(self, areg_pow_led_statu: enums.AregPlEd) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:CONDition \n
		Snippet: driver.source.areGenerator.channel.condition.set_value(areg_pow_led_statu = enums.AregPlEd.ERRor) \n
		Displays the status of the power LED for the related radar channel. \n
			:param areg_pow_led_statu: INACtive| WARNing| ERRor| OK INACtive The channel is inactive. The power LED lights grey. WARNing Displays a warning for the channel. The power LED lights yellow. ERRor Displays an error for the channel. The power LED lights red. OK The channel is active and works properly. The power LED lights green.
		"""
		param = Conversions.enum_scalar_to_str(areg_pow_led_statu, enums.AregPlEd)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:CONDition {param}')
