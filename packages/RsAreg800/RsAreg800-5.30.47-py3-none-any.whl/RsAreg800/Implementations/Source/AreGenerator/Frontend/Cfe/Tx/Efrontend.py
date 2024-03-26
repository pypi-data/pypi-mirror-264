from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EfrontendCls:
	"""Efrontend commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("efrontend", core, parent)

	def set(self, instr_name: str, channel=repcap.Channel.Default, txIndexNull=repcap.TxIndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:TX<ST0>:EFRontend \n
		Snippet: driver.source.areGenerator.frontend.cfe.tx.efrontend.set(instr_name = 'abc', channel = repcap.Channel.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		No command help available \n
			:param instr_name: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
		"""
		param = Conversions.value_to_quoted_str(instr_name)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:TX{txIndexNull_cmd_val}:EFRontend {param}')

	def get(self, channel=repcap.Channel.Default, txIndexNull=repcap.TxIndexNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:TX<ST0>:EFRontend \n
		Snippet: value: str = driver.source.areGenerator.frontend.cfe.tx.efrontend.get(channel = repcap.Channel.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
			:return: instr_name: No help available"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:TX{txIndexNull_cmd_val}:EFRontend?')
		return trim_str_response(response)
