from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IpAddressCls:
	"""IpAddress commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ipAddress", core, parent)

	@property
	def subnet(self):
		"""subnet commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subnet'):
			from .Subnet import SubnetCls
			self._subnet = SubnetCls(self._core, self._cmd_group)
		return self._subnet

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.NetMode:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:IPADdress:MODE \n
		Snippet: value: enums.NetMode = driver.system.communicate.rt.network.ipAddress.get_mode() \n
		Selects manual or automatic setting of the IP address. \n
			:return: zynq_mode: AUTO| STATic
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:RT:NETWork:IPADdress:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.NetMode)

	def set_mode(self, zynq_mode: enums.NetMode) -> None:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:IPADdress:MODE \n
		Snippet: driver.system.communicate.rt.network.ipAddress.set_mode(zynq_mode = enums.NetMode.AUTO) \n
		Selects manual or automatic setting of the IP address. \n
			:param zynq_mode: AUTO| STATic
		"""
		param = Conversions.enum_scalar_to_str(zynq_mode, enums.NetMode)
		self._core.io.write(f'SYSTem:COMMunicate:RT:NETWork:IPADdress:MODE {param}')

	def get_value(self) -> bytes:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:IPADdress \n
		Snippet: value: bytes = driver.system.communicate.rt.network.ipAddress.get_value() \n
		Sets the IP address. \n
			:return: areg_zynq_net_ip_address: No help available
		"""
		response = self._core.io.query_bin_block('SYSTem:COMMunicate:RT:NETWork:IPADdress?')
		return response

	def set_value(self, areg_zynq_net_ip_address: bytes) -> None:
		"""SCPI: SYSTem:COMMunicate:RT:NETWork:IPADdress \n
		Snippet: driver.system.communicate.rt.network.ipAddress.set_value(areg_zynq_net_ip_address = b'ABCDEFGH') \n
		Sets the IP address. \n
			:param areg_zynq_net_ip_address: No help available
		"""
		self._core.io.write_bin_block('SYSTem:COMMunicate:RT:NETWork:IPADdress ', areg_zynq_net_ip_address)

	def clone(self) -> 'IpAddressCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IpAddressCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
