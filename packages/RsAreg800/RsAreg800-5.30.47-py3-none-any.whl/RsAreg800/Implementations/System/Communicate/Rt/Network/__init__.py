from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NetworkCls:
	"""Network commands group definition. 8 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("network", core, parent)

	@property
	def ipAddress(self):
		"""ipAddress commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_ipAddress'):
			from .IpAddress import IpAddressCls
			self._ipAddress = IpAddressCls(self._core, self._cmd_group)
		return self._ipAddress

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_restart'):
			from .Restart import RestartCls
			self._restart = RestartCls(self._core, self._cmd_group)
		return self._restart

	@property
	def common(self):
		"""common commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_common'):
			from .Common import CommonCls
			self._common = CommonCls(self._core, self._cmd_group)
		return self._common

	def get_mac_address(self) -> str:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:MACaddress \n
		Snippet: value: str = driver.system.communicate.rt.network.get_mac_address() \n
		Queries the MAC address of the instrument connected to the R&S AREG800A via the realtime control interface. \n
			:return: zynq_mac_address: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:RT:NETWork:MACaddress?')
		return trim_str_response(response)

	def set_mac_address(self, zynq_mac_address: str) -> None:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:MACaddress \n
		Snippet: driver.system.communicate.rt.network.set_mac_address(zynq_mac_address = 'abc') \n
		Queries the MAC address of the instrument connected to the R&S AREG800A via the realtime control interface. \n
			:param zynq_mac_address: string
		"""
		param = Conversions.value_to_quoted_str(zynq_mac_address)
		self._core.io.write(f'SYSTem:COMMunicate:RT:NETWork:MACaddress {param}')

	def get_status(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:STATus \n
		Snippet: value: bool = driver.system.communicate.rt.network.get_status() \n
		Queries the network configuration state. \n
			:return: zynq_net_status: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:RT:NETWork:STATus?')
		return Conversions.str_to_bool(response)

	def set_status(self, zynq_net_status: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:STATus \n
		Snippet: driver.system.communicate.rt.network.set_status(zynq_net_status = False) \n
		Queries the network configuration state. \n
			:param zynq_net_status: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(zynq_net_status)
		self._core.io.write(f'SYSTem:COMMunicate:RT:NETWork:STATus {param}')

	def clone(self) -> 'NetworkCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NetworkCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
