from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OtimeCls:
	"""Otime commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("otime", core, parent)

	def set(self, areg_adjust_otime: int, mappingChannel=repcap.MappingChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:ADJust:LEVel:OTIMe \n
		Snippet: driver.source.areGenerator.mapping.adjust.level.otime.set(areg_adjust_otime = 1, mappingChannel = repcap.MappingChannel.Default) \n
		Sets the observation time to determine peaks of the channel output power level. \n
			:param areg_adjust_otime: integer Range: 10 to 10000
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
		"""
		param = Conversions.decimal_value_to_str(areg_adjust_otime)
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:ADJust:LEVel:OTIMe {param}')

	def get(self, mappingChannel=repcap.MappingChannel.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:ADJust:LEVel:OTIMe \n
		Snippet: value: int = driver.source.areGenerator.mapping.adjust.level.otime.get(mappingChannel = repcap.MappingChannel.Default) \n
		Sets the observation time to determine peaks of the channel output power level. \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:return: areg_adjust_otime: integer Range: 10 to 10000"""
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:ADJust:LEVel:OTIMe?')
		return Conversions.str_to_int(response)
