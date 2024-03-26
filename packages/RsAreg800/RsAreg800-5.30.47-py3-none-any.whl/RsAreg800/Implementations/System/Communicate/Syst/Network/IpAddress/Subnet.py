from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubnetCls:
	"""Subnet commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subnet", core, parent)

	def get_mask(self) -> bytes:
		"""SCPI: SYSTem:COMMunicate:SYST:NETWork:[IPADdress]:SUBNet:MASK \n
		Snippet: value: bytes = driver.system.communicate.syst.network.ipAddress.subnet.get_mask() \n
		Sets the subnet mask. \n
			:return: areg_zynq_net_sub_net_mask: No help available
		"""
		response = self._core.io.query_bin_block('SYSTem:COMMunicate:SYST:NETWork:IPADdress:SUBNet:MASK?')
		return response

	def set_mask(self, areg_zynq_net_sub_net_mask: bytes) -> None:
		"""SCPI: SYSTem:COMMunicate:SYST:NETWork:[IPADdress]:SUBNet:MASK \n
		Snippet: driver.system.communicate.syst.network.ipAddress.subnet.set_mask(areg_zynq_net_sub_net_mask = b'ABCDEFGH') \n
		Sets the subnet mask. \n
			:param areg_zynq_net_sub_net_mask: No help available
		"""
		self._core.io.write_bin_block('SYSTem:COMMunicate:SYST:NETWork:IPADdress:SUBNet:MASK ', areg_zynq_net_sub_net_mask)
