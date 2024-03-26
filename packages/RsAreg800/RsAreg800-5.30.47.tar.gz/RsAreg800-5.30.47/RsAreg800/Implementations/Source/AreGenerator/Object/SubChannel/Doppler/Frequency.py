from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, areg_ob_dopp_freq: float, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:DOPPler:FREQuency \n
		Snippet: driver.source.areGenerator.object.subChannel.doppler.frequency.set(areg_ob_dopp_freq = 1.0, objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:DOPPler FREQuency. Sets the doppler shift of the simulated radar object. \n
			:param areg_ob_dopp_freq: float Range: depends on settings to depends on settings
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
		"""
		param = Conversions.decimal_value_to_str(areg_ob_dopp_freq)
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:DOPPler:FREQuency {param}')

	def get(self, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:DOPPler:FREQuency \n
		Snippet: value: float = driver.source.areGenerator.object.subChannel.doppler.frequency.get(objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:DOPPler FREQuency. Sets the doppler shift of the simulated radar object. \n
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:return: areg_ob_dopp_freq: float Range: depends on settings to depends on settings"""
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:DOPPler:FREQuency?')
		return Conversions.str_to_float(response)
