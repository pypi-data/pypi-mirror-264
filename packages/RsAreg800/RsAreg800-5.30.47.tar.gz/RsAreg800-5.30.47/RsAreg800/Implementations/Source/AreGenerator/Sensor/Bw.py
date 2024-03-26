from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwCls:
	"""Bw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bw", core, parent)

	def set(self, areg_sens_bw: int, sensor=repcap.Sensor.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:BW \n
		Snippet: driver.source.areGenerator.sensor.bw.set(areg_sens_bw = 1, sensor = repcap.Sensor.Default) \n
		Sets the bandwidth for the radar sensor. Set it according to the bandwith of the radar sensor included in the test setup. \n
			:param areg_sens_bw: integer Range: 0 to 10E9
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
		"""
		param = Conversions.decimal_value_to_str(areg_sens_bw)
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:BW {param}')

	def get(self, sensor=repcap.Sensor.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:BW \n
		Snippet: value: int = driver.source.areGenerator.sensor.bw.get(sensor = repcap.Sensor.Default) \n
		Sets the bandwidth for the radar sensor. Set it according to the bandwith of the radar sensor included in the test setup. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: areg_sens_bw: integer Range: 0 to 10E9"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:BW?')
		return Conversions.str_to_int(response)
