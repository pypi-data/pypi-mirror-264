from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SensorCls:
	"""Sensor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sensor", core, parent)

	def set(self, areg_mapping_mts: enums.AregChanMappingSensor, mappingChannel=repcap.MappingChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:SENSor \n
		Snippet: driver.source.areGenerator.mapping.sensor.set(areg_mapping_mts = enums.AregChanMappingSensor.NONE, mappingChannel = repcap.MappingChannel.Default) \n
		Selects the sensor that is mapped to the radar channel. \n
			:param areg_mapping_mts: NONE| SEN1| SEN2| SEN4| SEN3| SEN5| SEN6| SEN7| SEN8 NONE No sensor is mapped. SEN1|SEN2|SEN4|SEN3|SEN5|SEN6|SEN7|SEN8 Selects the respective sensor and maps it to the radar channel.
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
		"""
		param = Conversions.enum_scalar_to_str(areg_mapping_mts, enums.AregChanMappingSensor)
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:SENSor {param}')

	# noinspection PyTypeChecker
	def get(self, mappingChannel=repcap.MappingChannel.Default) -> enums.AregChanMappingSensor:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:SENSor \n
		Snippet: value: enums.AregChanMappingSensor = driver.source.areGenerator.mapping.sensor.get(mappingChannel = repcap.MappingChannel.Default) \n
		Selects the sensor that is mapped to the radar channel. \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:return: areg_mapping_mts: NONE| SEN1| SEN2| SEN4| SEN3| SEN5| SEN6| SEN7| SEN8 NONE No sensor is mapped. SEN1|SEN2|SEN4|SEN3|SEN5|SEN6|SEN7|SEN8 Selects the respective sensor and maps it to the radar channel."""
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:SENSor?')
		return Conversions.str_to_scalar_enum(response, enums.AregChanMappingSensor)
