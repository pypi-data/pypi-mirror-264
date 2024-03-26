from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DistanceCls:
	"""Distance commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("distance", core, parent)

	def set(self, areg_sens_sto_distance: int, sensor=repcap.Sensor.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:DISTance \n
		Snippet: driver.source.areGenerator.sensor.distance.set(areg_sens_sto_distance = 1, sensor = repcap.Sensor.Default) \n
		Sets the relative distance between radar sensor and origin. \n
			:param areg_sens_sto_distance: integer Range: 0 to 30
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
		"""
		param = Conversions.decimal_value_to_str(areg_sens_sto_distance)
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:DISTance {param}')

	def get(self, sensor=repcap.Sensor.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:DISTance \n
		Snippet: value: int = driver.source.areGenerator.sensor.distance.get(sensor = repcap.Sensor.Default) \n
		Sets the relative distance between radar sensor and origin. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: areg_sens_sto_distance: integer Range: 0 to 30"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:DISTance?')
		return Conversions.str_to_int(response)
