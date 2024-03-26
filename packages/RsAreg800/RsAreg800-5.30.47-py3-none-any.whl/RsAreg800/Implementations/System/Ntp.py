from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NtpCls:
	"""Ntp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ntp", core, parent)

	def get_hostname(self) -> str:
		"""SCPI: SYSTem:NTP:HOSTname \n
		Snippet: value: str = driver.system.ntp.get_hostname() \n
		Sets the address of the NTP server. You can enter the IP address, or the hostname of the time server, or even set up an
		own vendor zone. See the Internet for more information on NTP. \n
			:return: ntp_name: string
		"""
		response = self._core.io.query_str('SYSTem:NTP:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, ntp_name: str) -> None:
		"""SCPI: SYSTem:NTP:HOSTname \n
		Snippet: driver.system.ntp.set_hostname(ntp_name = 'abc') \n
		Sets the address of the NTP server. You can enter the IP address, or the hostname of the time server, or even set up an
		own vendor zone. See the Internet for more information on NTP. \n
			:param ntp_name: string
		"""
		param = Conversions.value_to_quoted_str(ntp_name)
		self._core.io.write(f'SYSTem:NTP:HOSTname {param}')
