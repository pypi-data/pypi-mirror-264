from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OmonitoringCls:
	"""Omonitoring commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("omonitoring", core, parent)

	def get_hostname(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:OMONitoring:HOSTname \n
		Snippet: value: str = driver.source.areGenerator.omonitoring.get_hostname() \n
		Sets hostname or IP address of the host (external PC) where the objects get streamed to. \n
			:return: mon_hostname: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OMONitoring:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, mon_hostname: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OMONitoring:HOSTname \n
		Snippet: driver.source.areGenerator.omonitoring.set_hostname(mon_hostname = 'abc') \n
		Sets hostname or IP address of the host (external PC) where the objects get streamed to. \n
			:param mon_hostname: string
		"""
		param = Conversions.value_to_quoted_str(mon_hostname)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OMONitoring:HOSTname {param}')

	def get_port(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:OMONitoring:PORT \n
		Snippet: value: int = driver.source.areGenerator.omonitoring.get_port() \n
		Sets the port of the host (external PC) where the objects get streamed to. \n
			:return: mon_port: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OMONitoring:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, mon_port: int) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OMONitoring:PORT \n
		Snippet: driver.source.areGenerator.omonitoring.set_port(mon_port = 1) \n
		Sets the port of the host (external PC) where the objects get streamed to. \n
			:param mon_port: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(mon_port)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OMONitoring:PORT {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:AREGenerator:OMONitoring:[STATe] \n
		Snippet: value: bool = driver.source.areGenerator.omonitoring.get_state() \n
		Sets the streaming state. \n
			:return: mon_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OMONitoring:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, mon_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OMONitoring:[STATe] \n
		Snippet: driver.source.areGenerator.omonitoring.set_state(mon_state = False) \n
		Sets the streaming state. \n
			:param mon_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(mon_state)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OMONitoring:STATe {param}')
