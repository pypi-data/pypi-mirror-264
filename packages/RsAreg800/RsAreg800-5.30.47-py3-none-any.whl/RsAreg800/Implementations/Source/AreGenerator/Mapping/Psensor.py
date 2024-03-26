from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PsensorCls:
	"""Psensor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("psensor", core, parent)

	def set(self, areg_mapping_ps_enable: enums.AregChanMappingSensor, mappingChannel=repcap.MappingChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:PSENsor \n
		Snippet: driver.source.areGenerator.mapping.psensor.set(areg_mapping_ps_enable = enums.AregChanMappingSensor.NONE, mappingChannel = repcap.MappingChannel.Default) \n
		No command help available \n
			:param areg_mapping_ps_enable: No help available
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
		"""
		param = Conversions.enum_scalar_to_str(areg_mapping_ps_enable, enums.AregChanMappingSensor)
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:PSENsor {param}')

	# noinspection PyTypeChecker
	def get(self, mappingChannel=repcap.MappingChannel.Default) -> enums.AregChanMappingSensor:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:PSENsor \n
		Snippet: value: enums.AregChanMappingSensor = driver.source.areGenerator.mapping.psensor.get(mappingChannel = repcap.MappingChannel.Default) \n
		No command help available \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:return: areg_mapping_ps_enable: No help available"""
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:PSENsor?')
		return Conversions.str_to_scalar_enum(response, enums.AregChanMappingSensor)
