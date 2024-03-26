from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MeasurementCls:
	"""Measurement commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	def get_keep_settings(self) -> bool:
		"""SCPI: [SOURce<HW>]:AREGenerator:MEASurement:KEEPsettings \n
		Snippet: value: bool = driver.source.areGenerator.measurement.get_keep_settings() \n
		Keeps the configurations and connection settings of connected external frontends if preset is activated. \n
			:return: keep_settings: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:MEASurement:KEEPsettings?')
		return Conversions.str_to_bool(response)

	def set_keep_settings(self, keep_settings: bool) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MEASurement:KEEPsettings \n
		Snippet: driver.source.areGenerator.measurement.set_keep_settings(keep_settings = False) \n
		Keeps the configurations and connection settings of connected external frontends if preset is activated. \n
			:param keep_settings: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(keep_settings)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MEASurement:KEEPsettings {param}')
