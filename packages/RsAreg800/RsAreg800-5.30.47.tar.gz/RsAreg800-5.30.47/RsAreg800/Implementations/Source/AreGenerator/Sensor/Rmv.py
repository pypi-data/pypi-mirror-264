from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RmvCls:
	"""Rmv commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rmv", core, parent)

	def set(self, sensor=repcap.Sensor.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:RMV \n
		Snippet: driver.source.areGenerator.sensor.rmv.set(sensor = repcap.Sensor.Default) \n
		Removes the configuration of the radar sensor from the list. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
		"""
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:RMV')

	def set_with_opc(self, sensor=repcap.Sensor.Default, opc_timeout_ms: int = -1) -> None:
		sensor_cmd_val = self._cmd_group.get_repcap_cmd_value(sensor, repcap.Sensor)
		"""SCPI: [SOURce<HW>]:AREGenerator:SENSor<CH>:RMV \n
		Snippet: driver.source.areGenerator.sensor.rmv.set_with_opc(sensor = repcap.Sensor.Default) \n
		Removes the configuration of the radar sensor from the list. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param sensor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sensor')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:SENSor{sensor_cmd_val}:RMV', opc_timeout_ms)
