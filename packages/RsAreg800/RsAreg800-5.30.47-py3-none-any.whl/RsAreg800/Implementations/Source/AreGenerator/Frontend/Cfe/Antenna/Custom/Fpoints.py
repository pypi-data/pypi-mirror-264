from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FpointsCls:
	"""Fpoints commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fpoints", core, parent)

	def set(self, areg_fe_cust_ant_fp: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ANTenna:CUSTom:FPOints \n
		Snippet: driver.source.areGenerator.frontend.cfe.antenna.custom.fpoints.set(areg_fe_cust_ant_fp = 1, channel = repcap.Channel.Default) \n
		Sets the number of frequencies that you want to define in the list. \n
			:param areg_fe_cust_ant_fp: integer Range: 1 to 512
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_cust_ant_fp)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ANTenna:CUSTom:FPOints {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ANTenna:CUSTom:FPOints \n
		Snippet: value: int = driver.source.areGenerator.frontend.cfe.antenna.custom.fpoints.get(channel = repcap.Channel.Default) \n
		Sets the number of frequencies that you want to define in the list. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:return: areg_fe_cust_ant_fp: integer Range: 1 to 512"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ANTenna:CUSTom:FPOints?')
		return Conversions.str_to_int(response)
