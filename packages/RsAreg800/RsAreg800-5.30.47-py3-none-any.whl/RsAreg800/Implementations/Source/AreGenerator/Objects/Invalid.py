from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InvalidCls:
	"""Invalid commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("invalid", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJects:INValid:CATalog \n
		Snippet: value: List[str] = driver.source.areGenerator.objects.invalid.get_catalog() \n
		Queries the content of the 'Invalid objects' table. Lists the header and all values for the respective object number. \n
			:return: areg_obj_invalid_cat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OBJects:INValid:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJects:INValid \n
		Snippet: value: int = driver.source.areGenerator.objects.invalid.get_value() \n
		Specifies the number of invalid radar objects for a specific channel. \n
			:return: numb_of_invalid_ob: integer Range: 0 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OBJects:INValid?')
		return Conversions.str_to_int(response)
