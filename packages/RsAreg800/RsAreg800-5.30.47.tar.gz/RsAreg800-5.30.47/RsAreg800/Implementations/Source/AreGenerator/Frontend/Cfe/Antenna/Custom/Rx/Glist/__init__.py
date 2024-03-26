from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GlistCls:
	"""Glist commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("glist", core, parent)

	@property
	def row(self):
		"""row commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	def set(self, areg_fconf_use_cust_ant_gain_list: List[float], channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ANTenna:CUSTom:RX<ST>:GLISt \n
		Snippet: driver.source.areGenerator.frontend.cfe.antenna.custom.rx.glist.set(areg_fconf_use_cust_ant_gain_list = [1.1, 2.2, 3.3], channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default) \n
		For TRX-type frontend: Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>:ANTenna:CUSTom[:MODE] LIST. Sets the values
		for antenna gain RX/TX in the list. Enter all values of the list separated by comma. \n
			:param areg_fconf_use_cust_ant_gain_list: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
		"""
		param = Conversions.list_to_csv_str(areg_fconf_use_cust_ant_gain_list)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ANTenna:CUSTom:RX{rxIndex_cmd_val}:GLISt {param}')

	def get(self, channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default) -> List[float]:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ANTenna:CUSTom:RX<ST>:GLISt \n
		Snippet: value: List[float] = driver.source.areGenerator.frontend.cfe.antenna.custom.rx.glist.get(channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default) \n
		For TRX-type frontend: Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>:ANTenna:CUSTom[:MODE] LIST. Sets the values
		for antenna gain RX/TX in the list. Enter all values of the list separated by comma. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: areg_fconf_use_cust_ant_gain_list: No help available"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_bin_or_ascii_float_list(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ANTenna:CUSTom:RX{rxIndex_cmd_val}:GLISt?')
		return response

	def clone(self) -> 'GlistCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GlistCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
