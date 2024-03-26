from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IdCls:
	"""Id commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("id", core, parent)

	def set(self, areg_sconf_dyn_id: int, sensor=repcap.Sensor.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:DYNamic:ID \n
		Snippet: driver.source.areGenerator.sensor.dynamic.id.set(areg_sconf_dyn_id = 1, sensor = repcap.Sensor.Default) \n
		Requires: [:SOURce<hw>]:AREGenerator:OSETup:REFerence MAPPed. Sets the ID of the radar sensor according to the definition
		in the used protocol, e.g. in a ZMQ OSI HiL protocol. The mapping is defined in the object list of the used protocol, e.g.
		the 'sensor_id' field in the osi3::sensorData struct for all OSI protocols. \n
			:param areg_sconf_dyn_id: integer Range: 0 to 1000
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
		"""
		param = Conversions.decimal_value_to_str(areg_sconf_dyn_id)
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:DYNamic:ID {param}')

	def get(self, sensor=repcap.Sensor.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:DYNamic:ID \n
		Snippet: value: int = driver.source.areGenerator.sensor.dynamic.id.get(sensor = repcap.Sensor.Default) \n
		Requires: [:SOURce<hw>]:AREGenerator:OSETup:REFerence MAPPed. Sets the ID of the radar sensor according to the definition
		in the used protocol, e.g. in a ZMQ OSI HiL protocol. The mapping is defined in the object list of the used protocol, e.g.
		the 'sensor_id' field in the osi3::sensorData struct for all OSI protocols. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: areg_sconf_dyn_id: integer Range: 0 to 1000"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:DYNamic:ID?')
		return Conversions.str_to_int(response)
