from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CenterCls:
	"""Center commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("center", core, parent)

	def set(self, areg_sens_cent_fre: int, sensor=repcap.Sensor.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:CENTer \n
		Snippet: driver.source.areGenerator.sensor.center.set(areg_sens_cent_fre = 1, sensor = repcap.Sensor.Default) \n
		Sets the center frequency for the radar sensor. Set it according to the center frequency of the radar sensor included in
		the test setup. \n
			:param areg_sens_cent_fre: integer Range: depends on settings to depends on settings
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
		"""
		param = Conversions.decimal_value_to_str(areg_sens_cent_fre)
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:CENTer {param}')

	def get(self, sensor=repcap.Sensor.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:CENTer \n
		Snippet: value: int = driver.source.areGenerator.sensor.center.get(sensor = repcap.Sensor.Default) \n
		Sets the center frequency for the radar sensor. Set it according to the center frequency of the radar sensor included in
		the test setup. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: areg_sens_cent_fre: integer Range: depends on settings to depends on settings"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:CENTer?')
		return Conversions.str_to_int(response)
