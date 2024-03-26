from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RowCls:
	"""Row commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: Index, default value after init: Index.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("row", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_index_get', 'repcap_index_set', repcap.Index.Nr1)

	def repcap_index_set(self, index: repcap.Index) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Index.Default
		Default value after init: Index.Nr1"""
		self._cmd_group.set_repcap_enum_value(index)

	def repcap_index_get(self) -> repcap.Index:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, gain: int, channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default, index=repcap.Index.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ANTenna:CUSTom:RX<ST>:GLISt:ROW<DI> \n
		Snippet: driver.source.areGenerator.frontend.cfe.antenna.custom.rx.glist.row.set(gain = 1, channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default, index = repcap.Index.Default) \n
		Sets the value for antenna gain RX/TX in the selected row of the list. \n
			:param gain: integer Range: -50 to 50
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
		"""
		param = Conversions.decimal_value_to_str(gain)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ANTenna:CUSTom:RX{rxIndex_cmd_val}:GLISt:ROW{index_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default, index=repcap.Index.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ANTenna:CUSTom:RX<ST>:GLISt:ROW<DI> \n
		Snippet: value: int = driver.source.areGenerator.frontend.cfe.antenna.custom.rx.glist.row.get(channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default, index = repcap.Index.Default) \n
		Sets the value for antenna gain RX/TX in the selected row of the list. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:return: gain: integer Range: -50 to 50"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ANTenna:CUSTom:RX{rxIndex_cmd_val}:GLISt:ROW{index_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'RowCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RowCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
