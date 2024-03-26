from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpeedCls:
	"""Speed commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("speed", core, parent)

	def set(self, areg_object_dopp: float, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:DOPPler:[SPEed] \n
		Snippet: driver.source.areGenerator.object.subChannel.doppler.speed.set(areg_object_dopp = 1.0, objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:DOPPler SPEed. Sets the Doppler speed of the simulated radar object. \n
			:param areg_object_dopp: float Range: -500 to 500
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
		"""
		param = Conversions.decimal_value_to_str(areg_object_dopp)
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:DOPPler:SPEed {param}')

	def get(self, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:DOPPler:[SPEed] \n
		Snippet: value: float = driver.source.areGenerator.object.subChannel.doppler.speed.get(objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:DOPPler SPEed. Sets the Doppler speed of the simulated radar object. \n
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:return: areg_object_dopp: float Range: -500 to 500"""
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:DOPPler:SPEed?')
		return Conversions.str_to_float(response)
