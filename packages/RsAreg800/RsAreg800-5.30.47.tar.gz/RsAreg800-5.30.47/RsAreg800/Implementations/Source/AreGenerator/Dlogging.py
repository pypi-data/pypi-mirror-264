from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DloggingCls:
	"""Dlogging commands group definition. 8 total commands, 0 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dlogging", core, parent)

	def clear(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:CLEar \n
		Snippet: driver.source.areGenerator.dlogging.clear() \n
		Removes all logging information, that is collected in the logging data. Query logging data via the command
		[:SOURce<hw>]:AREGenerator:DLOGging:DATA. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:DLOGging:CLEar')

	def clear_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:CLEar \n
		Snippet: driver.source.areGenerator.dlogging.clear_with_opc() \n
		Removes all logging information, that is collected in the logging data. Query logging data via the command
		[:SOURce<hw>]:AREGenerator:DLOGging:DATA. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:DLOGging:CLEar', opc_timeout_ms)

	def get_data(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:DATA \n
		Snippet: value: List[str] = driver.source.areGenerator.dlogging.get_data() \n
		Queries all logging information in the logged data. \n
			:return: areg_dyn_logg_data: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:DLOGging:DATA?')
		return Conversions.str_to_str_list(response)

	# noinspection PyTypeChecker
	def get_level(self) -> enums.AregDynLoggLevel:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:LEVel \n
		Snippet: value: enums.AregDynLoggLevel = driver.source.areGenerator.dlogging.get_level() \n
		Defines the scope of logged data. Only logging information is collected, that corresponds to this scope. \n
			:return: dyn_logg_level: ALL| EAWarning| ERRor All Logged data includes information on errors, warnings and info messages. EAWarning Logged data includes information on errors and warnings. ERRor Logged data includes information on errors.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:DLOGging:LEVel?')
		return Conversions.str_to_scalar_enum(response, enums.AregDynLoggLevel)

	def set_level(self, dyn_logg_level: enums.AregDynLoggLevel) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:LEVel \n
		Snippet: driver.source.areGenerator.dlogging.set_level(dyn_logg_level = enums.AregDynLoggLevel.ALL) \n
		Defines the scope of logged data. Only logging information is collected, that corresponds to this scope. \n
			:param dyn_logg_level: ALL| EAWarning| ERRor All Logged data includes information on errors, warnings and info messages. EAWarning Logged data includes information on errors and warnings. ERRor Logged data includes information on errors.
		"""
		param = Conversions.enum_scalar_to_str(dyn_logg_level, enums.AregDynLoggLevel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:DLOGging:LEVel {param}')

	def get_nerror(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:NERRor \n
		Snippet: value: int = driver.source.areGenerator.dlogging.get_nerror() \n
		Queries the number of errors within the logged data. \n
			:return: dyn_logg_num_of_err: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:DLOGging:NERRor?')
		return Conversions.str_to_int(response)

	def get_ninfo(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:NINFo \n
		Snippet: value: int = driver.source.areGenerator.dlogging.get_ninfo() \n
		Queries the number of info messages within the logged data. \n
			:return: dyn_logg_num_of_inf: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:DLOGging:NINFo?')
		return Conversions.str_to_int(response)

	def get_nwarning(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:NWARning \n
		Snippet: value: int = driver.source.areGenerator.dlogging.get_nwarning() \n
		Queries the number of warnings within the logged data. \n
			:return: dyn_logg_num_of_war: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:DLOGging:NWARning?')
		return Conversions.str_to_int(response)

	def get_save(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:SAVE \n
		Snippet: value: str = driver.source.areGenerator.dlogging.get_save() \n
		Saves logged data to a file with file extension *.csv. The file extension is added automatically. \n
			:return: dyn_logg_save: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:DLOGging:SAVE?')
		return trim_str_response(response)

	def set_save(self, dyn_logg_save: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:SAVE \n
		Snippet: driver.source.areGenerator.dlogging.set_save(dyn_logg_save = 'abc') \n
		Saves logged data to a file with file extension *.csv. The file extension is added automatically. \n
			:param dyn_logg_save: string
		"""
		param = Conversions.value_to_quoted_str(dyn_logg_save)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:DLOGging:SAVE {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:[STATe] \n
		Snippet: value: bool = driver.source.areGenerator.dlogging.get_state() \n
		Activates logging. \n
			:return: dyn_logg_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:DLOGging:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, dyn_logg_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:DLOGging:[STATe] \n
		Snippet: driver.source.areGenerator.dlogging.set_state(dyn_logg_state = False) \n
		Activates logging. \n
			:param dyn_logg_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(dyn_logg_state)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:DLOGging:STATe {param}')
