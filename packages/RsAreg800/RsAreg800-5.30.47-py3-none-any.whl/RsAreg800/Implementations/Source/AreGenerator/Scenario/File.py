from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:FILE:CATalog \n
		Snippet: value: List[str] = driver.source.areGenerator.scenario.file.get_catalog() \n
		Queries the available scenario files. Lists all *.osi and *.sm files available in the default directory /var/user/. \n
			:return: areg_scenario_file_cat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SCENario:FILE:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:FILE \n
		Snippet: value: str = driver.source.areGenerator.scenario.file.get_value() \n
		Selects an existing scenario file from the default directory or from a specific directory. \n
			:return: scenario_file: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SCENario:FILE?')
		return trim_str_response(response)

	def set_value(self, scenario_file: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:FILE \n
		Snippet: driver.source.areGenerator.scenario.file.set_value(scenario_file = 'abc') \n
		Selects an existing scenario file from the default directory or from a specific directory. \n
			:param scenario_file: string
		"""
		param = Conversions.value_to_quoted_str(scenario_file)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:FILE {param}')
