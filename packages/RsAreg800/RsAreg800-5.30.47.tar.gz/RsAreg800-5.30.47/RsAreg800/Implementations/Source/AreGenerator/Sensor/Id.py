from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IdCls:
	"""Id commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("id", core, parent)

	def get(self, sensor=repcap.Sensor.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:ID \n
		Snippet: value: int = driver.source.areGenerator.sensor.id.get(sensor = repcap.Sensor.Default) \n
		Queries the identification name of the radar sensor. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: areg_sens_id: integer Range: 0 to 1000"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:ID?')
		return Conversions.str_to_int(response)
