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

	def set(self, areg_fe_ota_offset: int, channel=repcap.Channel.Default, txIndexNull=repcap.TxIndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:TX<ST0>:OTA:OFFSet \n
		Snippet: driver.source.areGenerator.frontend.cfe.tx.ota.offset.set(areg_fe_ota_offset = 1, channel = repcap.Channel.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param areg_fe_ota_offset: integer Range: 0.01 to 30
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_ota_offset)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:TX{txIndexNull_cmd_val}:OTA:OFFSet {param}')

	def get(self, channel=repcap.Channel.Default, txIndexNull=repcap.TxIndexNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:TX<ST0>:OTA:OFFSet \n
		Snippet: value: int = driver.source.areGenerator.frontend.cfe.tx.ota.offset.get(channel = repcap.Channel.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
			:return: areg_fe_ota_offset: integer Range: 0.01 to 30"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:TX{txIndexNull_cmd_val}:OTA:OFFSet?')
		return Conversions.str_to_int(response)
