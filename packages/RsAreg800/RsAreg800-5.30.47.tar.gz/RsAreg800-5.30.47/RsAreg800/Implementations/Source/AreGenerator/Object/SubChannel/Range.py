from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RangeCls:
	"""Range commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("range", core, parent)

	def get(self, objectIx=repcap.ObjectIx.Default, subchannel=repcap.Subchannel.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:OBJect<CH>:[SUBChannel<ST>]:RANGe \n
		Snippet: value: float = driver.source.areGenerator.object.subChannel.range.get(objectIx = repcap.ObjectIx.Default, subchannel = repcap.Subchannel.Default) \n
		Sets the range of the simulated radar object. The range depends on the installed option and on the cable delay settings,
		the air gap and the bandwidth option. \n
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:return: areg_obj_range: float Range: depends on settings to depends on settings"""
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:OBJect{objectIx_cmd_val}:SUBChannel{subchannel_cmd_val}:RANGe?')
		return Conversions.str_to_float(response)
