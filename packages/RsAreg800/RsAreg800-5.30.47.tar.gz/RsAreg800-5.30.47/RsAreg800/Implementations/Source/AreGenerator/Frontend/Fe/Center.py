from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CenterCls:
	"""Center commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("center", core, parent)

	def set(self, areg_fe_center_fre: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:CENTer \n
		Snippet: driver.source.areGenerator.frontend.fe.center.set(areg_fe_center_fre = 1.0, channel = repcap.Channel.Default) \n
		Sets the RF center frequency of the output signal of the connected frontend. The frontend center frequency and frequency
		range depend on the configuration of the R&S AREG800A and the configuration of the frontend included in the test setup.
		For more information, see the data sheet. When using custom frontends, the IF center frequency instead of the RF center
		frequency is configurable in the frontend configuration. The IF center frequency with the sensor bandwidth is used for
		the cable correction, whereas the sensor frequency and bandwidth is used for the antenna correction. \n
			:param areg_fe_center_fre: float Range: 0 to 100E9
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_center_fre)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:CENTer {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:CENTer \n
		Snippet: value: float = driver.source.areGenerator.frontend.fe.center.get(channel = repcap.Channel.Default) \n
		Sets the RF center frequency of the output signal of the connected frontend. The frontend center frequency and frequency
		range depend on the configuration of the R&S AREG800A and the configuration of the frontend included in the test setup.
		For more information, see the data sheet. When using custom frontends, the IF center frequency instead of the RF center
		frequency is configurable in the frontend configuration. The IF center frequency with the sensor bandwidth is used for
		the cable correction, whereas the sensor frequency and bandwidth is used for the antenna correction. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:return: areg_fe_center_fre: float Range: 0 to 100E9"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:CENTer?')
		return Conversions.str_to_float(response)
