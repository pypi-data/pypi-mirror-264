from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RtsCls:
	"""Rts commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rts", core, parent)

	def set(self, areg_fe_rts: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:RTS \n
		Snippet: driver.source.areGenerator.frontend.fe.rts.set(areg_fe_rts = 1.0, channel = repcap.Channel.Default) \n
		Sets the rotation angle between frontend and sensor. Reference point for the definition of the angle is the center of the
		frontend. The rotation describes the deviation of the position of the frontend from a 90DEG angle to the direct line of
		sight of the sensor. For TRX-type or custom frontends this parameter has currently no impact, since it is a single sensor
		and no sensor array. \n
			:param areg_fe_rts: float Range: -60 to 60
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_rts)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:RTS {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:RTS \n
		Snippet: value: float = driver.source.areGenerator.frontend.fe.rts.get(channel = repcap.Channel.Default) \n
		Sets the rotation angle between frontend and sensor. Reference point for the definition of the angle is the center of the
		frontend. The rotation describes the deviation of the position of the frontend from a 90DEG angle to the direct line of
		sight of the sensor. For TRX-type or custom frontends this parameter has currently no impact, since it is a single sensor
		and no sensor array. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:return: areg_fe_rts: float Range: -60 to 60"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:RTS?')
		return Conversions.str_to_float(response)
