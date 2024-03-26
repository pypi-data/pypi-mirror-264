from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RmvCls:
	"""Rmv commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rmv", core, parent)

	def set(self, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:RMV \n
		Snippet: driver.source.areGenerator.frontend.cfe.rmv.set(channel = repcap.Channel.Default) \n
		Removes the configuration of the connected QAT-type, FE-type or custom frontend. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
		"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:RMV')

	def set_with_opc(self, channel=repcap.Channel.Default, opc_timeout_ms: int = -1) -> None:
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:RMV \n
		Snippet: driver.source.areGenerator.frontend.cfe.rmv.set_with_opc(channel = repcap.Channel.Default) \n
		Removes the configuration of the connected QAT-type, FE-type or custom frontend. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:RMV', opc_timeout_ms)
