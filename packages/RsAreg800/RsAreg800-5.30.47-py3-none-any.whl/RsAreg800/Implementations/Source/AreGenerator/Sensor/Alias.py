from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AliasCls:
	"""Alias commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alias", core, parent)

	def set(self, areg_sens_alias: str, sensor=repcap.Sensor.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:ALIas \n
		Snippet: driver.source.areGenerator.sensor.alias.set(areg_sens_alias = 'abc', sensor = repcap.Sensor.Default) \n
		Sets the alias of the radar sensor. \n
			:param areg_sens_alias: string
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
		"""
		param = Conversions.value_to_quoted_str(areg_sens_alias)
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:ALIas {param}')

	def get(self, sensor=repcap.Sensor.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:ALIas \n
		Snippet: value: str = driver.source.areGenerator.sensor.alias.get(sensor = repcap.Sensor.Default) \n
		Sets the alias of the radar sensor. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: areg_sens_alias: string"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:ALIas?')
		return trim_str_response(response)
