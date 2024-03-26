from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DigHeadroomCls:
	"""DigHeadroom commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("digHeadroom", core, parent)

	def set(self, areg_adjust_dhead: int, mappingChannel=repcap.MappingChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:ADJust:LEVel:DIGHeadroom \n
		Snippet: driver.source.areGenerator.mapping.adjust.level.digHeadroom.set(areg_adjust_dhead = 1, mappingChannel = repcap.MappingChannel.Default) \n
		Sets the digital headroom of the channel output power. \n
			:param areg_adjust_dhead: integer Range: 0 to 30
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
		"""
		param = Conversions.decimal_value_to_str(areg_adjust_dhead)
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:ADJust:LEVel:DIGHeadroom {param}')

	def get(self, mappingChannel=repcap.MappingChannel.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:ADJust:LEVel:DIGHeadroom \n
		Snippet: value: int = driver.source.areGenerator.mapping.adjust.level.digHeadroom.get(mappingChannel = repcap.MappingChannel.Default) \n
		Sets the digital headroom of the channel output power. \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:return: areg_adjust_dhead: integer Range: 0 to 30"""
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:ADJust:LEVel:DIGHeadroom?')
		return Conversions.str_to_int(response)
