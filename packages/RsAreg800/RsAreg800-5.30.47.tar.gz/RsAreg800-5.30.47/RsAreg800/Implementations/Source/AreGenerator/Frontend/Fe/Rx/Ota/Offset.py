from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, areg_fe_ota_offset: int, channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:RX<ST>:OTA:OFFSet \n
		Snippet: driver.source.areGenerator.frontend.fe.rx.ota.offset.set(areg_fe_ota_offset = 1, channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param areg_fe_ota_offset: integer Range: 0.01 to 30
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_ota_offset)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:RX{rxIndex_cmd_val}:OTA:OFFSet {param}')

	def get(self, channel=repcap.Channel.Default, rxIndex=repcap.RxIndex.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:RX<ST>:OTA:OFFSet \n
		Snippet: value: int = driver.source.areGenerator.frontend.fe.rx.ota.offset.get(channel = repcap.Channel.Default, rxIndex = repcap.RxIndex.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: areg_fe_ota_offset: integer Range: 0.01 to 30"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:RX{rxIndex_cmd_val}:OTA:OFFSet?')
		return Conversions.str_to_int(response)
