from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AttenuationCls:
	"""Attenuation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuation", core, parent)

	def set(self, areg_obj_att: float, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:ATTenuation \n
		Snippet: driver.source.areGenerator.object.subChannel.attenuation.set(areg_obj_att = 1.0, objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:KCONstant ATT. Sets the attenuation of the simulated radar object.
		The attenuation depends on the input power, i.e. a lower input signal can be amplified more. If the gain control reaches
		the upper limit, a message is displayed. \n
			:param areg_obj_att: float Range: -90 to 90
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
		"""
		param = Conversions.decimal_value_to_str(areg_obj_att)
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:ATTenuation {param}')

	def get(self, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:ATTenuation \n
		Snippet: value: float = driver.source.areGenerator.object.subChannel.attenuation.get(objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:KCONstant ATT. Sets the attenuation of the simulated radar object.
		The attenuation depends on the input power, i.e. a lower input signal can be amplified more. If the gain control reaches
		the upper limit, a message is displayed. \n
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:return: areg_obj_att: float Range: -90 to 90"""
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:ATTenuation?')
		return Conversions.str_to_float(response)
