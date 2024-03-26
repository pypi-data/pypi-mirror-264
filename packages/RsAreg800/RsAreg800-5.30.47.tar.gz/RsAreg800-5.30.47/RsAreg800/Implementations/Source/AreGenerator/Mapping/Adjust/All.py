from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllCls:
	"""All commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("all", core, parent)

	def set(self, mappingChannel=repcap.MappingChannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:ADJust:ALL \n
		Snippet: driver.source.areGenerator.mapping.adjust.all.set(mappingChannel = repcap.MappingChannel.Default) \n
		Adjusts the input attenuation of the R&S AREG800A for the applied signal automatically for all output channels. \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
		"""
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:ADJust:ALL')

	def set_with_opc(self, mappingChannel=repcap.MappingChannel.Default, opc_timeout_ms: int = -1) -> None:
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:ADJust:ALL \n
		Snippet: driver.source.areGenerator.mapping.adjust.all.set_with_opc(mappingChannel = repcap.MappingChannel.Default) \n
		Adjusts the input attenuation of the R&S AREG800A for the applied signal automatically for all output channels. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:ADJust:ALL', opc_timeout_ms)
