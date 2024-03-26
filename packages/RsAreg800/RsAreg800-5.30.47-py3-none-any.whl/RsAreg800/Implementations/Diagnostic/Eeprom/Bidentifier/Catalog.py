from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	def get(self, board_id: List[str], channel=repcap.Channel.Default) -> List[str]:
		"""SCPI: DIAGnostic<HW>:EEPRom<CH>:BIDentifier:CATalog \n
		Snippet: value: List[str] = driver.diagnostic.eeprom.bidentifier.catalog.get(board_id = ['abc1', 'abc2', 'abc3'], channel = repcap.Channel.Default) \n
		No command help available \n
			:param board_id: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eeprom')
			:return: board_id: No help available"""
		param = Conversions.list_to_csv_quoted_str(board_id)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'DIAGnostic<HwInstance>:EEPRom{channel_cmd_val}:BIDentifier:CATalog? {param}')
		return Conversions.str_to_str_list(response)
