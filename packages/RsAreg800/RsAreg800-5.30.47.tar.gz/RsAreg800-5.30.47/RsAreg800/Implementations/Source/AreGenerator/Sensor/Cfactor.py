from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfactorCls:
	"""Cfactor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfactor", core, parent)

	def set(self, areg_sens_crest_fa: float, sensor=repcap.Sensor.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:CFACtor \n
		Snippet: driver.source.areGenerator.sensor.cfactor.set(areg_sens_crest_fa = 1.0, sensor = repcap.Sensor.Default) \n
		Sets the crest factor for the signal. \n
			:param areg_sens_crest_fa: float Range: 0 to 100
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
		"""
		param = Conversions.decimal_value_to_str(areg_sens_crest_fa)
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:CFACtor {param}')

	def get(self, sensor=repcap.Sensor.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:CFACtor \n
		Snippet: value: float = driver.source.areGenerator.sensor.cfactor.get(sensor = repcap.Sensor.Default) \n
		Sets the crest factor for the signal. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:return: areg_sens_crest_fa: float Range: 0 to 100"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:CFACtor?')
		return Conversions.str_to_float(response)
