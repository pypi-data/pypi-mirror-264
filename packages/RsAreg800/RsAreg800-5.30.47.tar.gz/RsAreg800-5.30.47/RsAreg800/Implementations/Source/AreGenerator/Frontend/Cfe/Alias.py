from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AliasCls:
	"""Alias commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alias", core, parent)

	def set(self, areg_fe_alias: str, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ALIas \n
		Snippet: driver.source.areGenerator.frontend.cfe.alias.set(areg_fe_alias = 'abc', channel = repcap.Channel.Default) \n
		Sets the alias of the frontend. \n
			:param areg_fe_alias: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
		"""
		param = Conversions.value_to_quoted_str(areg_fe_alias)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ALIas {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ALIas \n
		Snippet: value: str = driver.source.areGenerator.frontend.cfe.alias.get(channel = repcap.Channel.Default) \n
		Sets the alias of the frontend. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:return: areg_fe_alias: string"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ALIas?')
		return trim_str_response(response)
