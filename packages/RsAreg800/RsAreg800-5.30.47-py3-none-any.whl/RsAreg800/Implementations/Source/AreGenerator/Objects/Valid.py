from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ValidCls:
	"""Valid commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("valid", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJects:VALid:CATalog \n
		Snippet: value: List[str] = driver.source.areGenerator.objects.valid.get_catalog() \n
		Queries the content of the 'valid objects' table. Lists the header and all values for the respective object number. \n
			:return: areg_obj_valid_cat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OBJects:VALid:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJects:VALid \n
		Snippet: value: int = driver.source.areGenerator.objects.valid.get_value() \n
		Specifies the number of valid radar objects f{umlaut}r a specific channel. \n
			:return: numb_of_valid_obj: integer Range: 0 to 64
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OBJects:VALid?')
		return Conversions.str_to_int(response)

	def set_value(self, numb_of_valid_obj: int) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJects:VALid \n
		Snippet: driver.source.areGenerator.objects.valid.set_value(numb_of_valid_obj = 1) \n
		Specifies the number of valid radar objects f{umlaut}r a specific channel. \n
			:param numb_of_valid_obj: integer Range: 0 to 64
		"""
		param = Conversions.decimal_value_to_str(numb_of_valid_obj)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OBJects:VALid {param}')
