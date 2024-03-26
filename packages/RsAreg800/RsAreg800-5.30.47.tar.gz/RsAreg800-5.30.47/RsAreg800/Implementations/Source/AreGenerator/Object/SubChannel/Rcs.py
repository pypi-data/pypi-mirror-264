from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RcsCls:
	"""Rcs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rcs", core, parent)

	def set(self, areg_obj_rcs: float, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:RCS \n
		Snippet: driver.source.areGenerator.object.subChannel.rcs.set(areg_obj_rcs = 1.0, objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:KCONstant RCS. Sets the radar cross section of the radar object. The radar
		cross section is calculated with the corresponding values for attenuation via the radar equation. \n
			:param areg_obj_rcs: float Range: -100 to 100
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
		"""
		param = Conversions.decimal_value_to_str(areg_obj_rcs)
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:RCS {param}')

	def get(self, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:RCS \n
		Snippet: value: float = driver.source.areGenerator.object.subChannel.rcs.get(objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:UNITs:KCONstant RCS. Sets the radar cross section of the radar object. The radar
		cross section is calculated with the corresponding values for attenuation via the radar equation. \n
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:return: areg_obj_rcs: float Range: -100 to 100"""
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:RCS?')
		return Conversions.str_to_float(response)
