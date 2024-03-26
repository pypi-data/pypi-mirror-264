from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CommonCls:
	"""Common commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("common", core, parent)

	def get_hostname(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SYST:NETWork:[COMMon]:HOSTname \n
		Snippet: value: str = driver.system.communicate.syst.network.common.get_hostname() \n
		Queries the hostname of the instrument connected to the R&S AREG800A via the system control interface. \n
			:return: zynq_hostname: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SYST:NETWork:COMMon:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, zynq_hostname: str) -> None:
		"""SCPI: SYSTem:COMMunicate:SYST:NETWork:[COMMon]:HOSTname \n
		Snippet: driver.system.communicate.syst.network.common.set_hostname(zynq_hostname = 'abc') \n
		Queries the hostname of the instrument connected to the R&S AREG800A via the system control interface. \n
			:param zynq_hostname: string
		"""
		param = Conversions.value_to_quoted_str(zynq_hostname)
		self._core.io.write(f'SYSTem:COMMunicate:SYST:NETWork:COMMon:HOSTname {param}')

	def get_workgroup(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SYST:NETWork:[COMMon]:WORKgroup \n
		Snippet: value: str = driver.system.communicate.syst.network.common.get_workgroup() \n
		No command help available \n
			:return: zynq_workgroup: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SYST:NETWork:COMMon:WORKgroup?')
		return trim_str_response(response)

	def set_workgroup(self, zynq_workgroup: str) -> None:
		"""SCPI: SYSTem:COMMunicate:SYST:NETWork:[COMMon]:WORKgroup \n
		Snippet: driver.system.communicate.syst.network.common.set_workgroup(zynq_workgroup = 'abc') \n
		No command help available \n
			:param zynq_workgroup: No help available
		"""
		param = Conversions.value_to_quoted_str(zynq_workgroup)
		self._core.io.write(f'SYSTem:COMMunicate:SYST:NETWork:COMMon:WORKgroup {param}')
