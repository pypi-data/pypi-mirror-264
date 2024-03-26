from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConfigCls:
	"""Config commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("config", core, parent)

	def get(self, mappingChannel=repcap.MappingChannel.Default, subchannel=repcap.Subchannel.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:MAPPing<CH>:[SUBChannel<ST>]:CONFig \n
		Snippet: value: str = driver.source.areGenerator.swunit.mapping.subChannel.config.get(mappingChannel = repcap.MappingChannel.Default, subchannel = repcap.Subchannel.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:SWUNit[:STATe] 1. Queries the channel RX / channel TX configuration between
		the switching unit and the R&S AREG800A. \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:return: areg_ext_sw_unit_con: No help available"""
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SWUNit:MAPPing{mappingChannel_cmd_val}:SUBChannel{subchannel_cmd_val}:CONFig?')
		return trim_str_response(response)
