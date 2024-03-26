from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwCls:
	"""Bw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bw", core, parent)

	def set(self, areg_fe_bw: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:BW \n
		Snippet: driver.source.areGenerator.frontend.fe.bw.set(areg_fe_bw = 1.0, channel = repcap.Channel.Default) \n
		Displays the frequency bandwidth of the output signal of the connected frontend. \n
			:param areg_fe_bw: float Range: 0 to 10E9
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_bw)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:BW {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:BW \n
		Snippet: value: float = driver.source.areGenerator.frontend.fe.bw.get(channel = repcap.Channel.Default) \n
		Displays the frequency bandwidth of the output signal of the connected frontend. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:return: areg_fe_bw: float Range: 0 to 10E9"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:BW?')
		return Conversions.str_to_float(response)
