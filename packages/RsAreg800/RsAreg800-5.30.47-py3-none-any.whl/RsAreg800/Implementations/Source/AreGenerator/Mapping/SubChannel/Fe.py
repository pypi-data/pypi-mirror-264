from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FeCls:
	"""Fe commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fe", core, parent)

	def set(self, areg_mapping_ctf: enums.AregChanMappingGui, mappingChannel=repcap.MappingChannel.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:[SUBChannel<ST>]:FE \n
		Snippet: driver.source.areGenerator.mapping.subChannel.fe.set(areg_mapping_ctf = enums.AregChanMappingGui.CFE1, mappingChannel = repcap.MappingChannel.Default, subchannel = repcap.Subchannel.Default) \n
		Maps the external frontend to the IF channel. \n
			:param areg_mapping_ctf: NONE| IFONly| TRX1| TRX2| TRX3| TRX4| QAT1CH1| QAT1CH2| QAT1CH3| QAT1CH4| QAT1CH5| QAT1CH6| QAT1CH7| QAT1CH8| QAT2CH1| QAT2CH2| QAT2CH3| QAT2CH4| QAT2CH5| QAT2CH6| QAT2CH7| QAT2CH8| QAT3CH1| QAT3CH2| QAT3CH3| QAT3CH4| QAT3CH5| QAT3CH6| QAT3CH7| QAT3CH8| QAT4CH1| QAT4CH2| QAT4CH3| QAT4CH4| QAT4CH5| QAT4CH6| QAT4CH7| QAT4CH8| QAT5CH1| QAT5CH2| QAT5CH3| QAT5CH4| QAT5CH5| QAT5CH6| QAT5CH7| QAT5CH8| QAT6CH1| QAT6CH2| QAT6CH3| QAT6CH4| QAT6CH5| QAT6CH6| QAT6CH7| QAT6CH8| QAT7CH1| QAT7CH2| QAT7CH3| QAT7CH4| QAT7CH5| QAT7CH6| QAT7CH7| QAT7CH8| QAT8CH1| QAT8CH2| QAT8CH3| QAT8CH4| QAT8CH5| QAT8CH6| QAT8CH7| QAT8CH8| FE1| FE2| FE3| FE4| CFE1| CFE2| CFE3| CFE4 NONE No frontend is mapped. IFONly Selects the IF interface without known frontend. TRX1|TRX2|TRX3|TRX4 Selects the TRX-type frontend and maps it to the respective radar channel. QAT1CH1|QAT1CH2|QAT1CH3|QAT1CH4|QAT1CH5|QAT1CH6|QAT1CH7|QAT1CH8|QAT2CH1|QAT2CH2|QAT2CH3|QAT2CH4|QAT2CH5|QAT2CH6|QAT2CH7|QAT2CH8|QAT3CH1|QAT3CH2|QAT3CH3|QAT3CH4|QAT3CH5|QAT3CH6|QAT3CH7|QAT3CH8|QAT4CH1|QAT4CH2|QAT4CH3|QAT4CH4|QAT4CH5|QAT4CH6|QAT4CH7|QAT4CH8|QAT5CH1|QAT5CH2|QAT5CH3|QAT5CH4|QAT5CH5|QAT5CH6|QAT5CH7|QAT5CH8|QAT6CH1|QAT6CH2|QAT6CH3|QAT6CH4|QAT6CH5|QAT6CH6|QAT6CH7|QAT6CH8|QAT7CH1|QAT7CH2|QAT7CH3|QAT7CH4|QAT7CH5|QAT7CH6|QAT7CH7|QAT7CH8|QAT8CH1|QAT8CH2|QAT8CH3|QAT8CH4|QAT8CH5|QAT8CH6|QAT8CH7|QAT8CH8 Selects the QAT-type frontend and maps it to the respective radar channel. FE1|FE2|FE3|FE4 Selects the FE-type frontend and maps it to the respective radar channel. CFE1|CFE2|CFE3|CFE4 Selects the custom frontend and maps it to the respective radar channel.
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
		"""
		param = Conversions.enum_scalar_to_str(areg_mapping_ctf, enums.AregChanMappingGui)
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:SUBChannel{subchannel_cmd_val}:FE {param}')

	# noinspection PyTypeChecker
	def get(self, mappingChannel=repcap.MappingChannel.Default, subchannel=repcap.Subchannel.Default) -> enums.AregChanMappingGui:
		"""SCPI: [SOURce<HW>]:AREGenerator:MAPPing<CH>:[SUBChannel<ST>]:FE \n
		Snippet: value: enums.AregChanMappingGui = driver.source.areGenerator.mapping.subChannel.fe.get(mappingChannel = repcap.MappingChannel.Default, subchannel = repcap.Subchannel.Default) \n
		Maps the external frontend to the IF channel. \n
			:param mappingChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mapping')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:return: areg_mapping_ctf: NONE| IFONly| TRX1| TRX2| TRX3| TRX4| QAT1CH1| QAT1CH2| QAT1CH3| QAT1CH4| QAT1CH5| QAT1CH6| QAT1CH7| QAT1CH8| QAT2CH1| QAT2CH2| QAT2CH3| QAT2CH4| QAT2CH5| QAT2CH6| QAT2CH7| QAT2CH8| QAT3CH1| QAT3CH2| QAT3CH3| QAT3CH4| QAT3CH5| QAT3CH6| QAT3CH7| QAT3CH8| QAT4CH1| QAT4CH2| QAT4CH3| QAT4CH4| QAT4CH5| QAT4CH6| QAT4CH7| QAT4CH8| QAT5CH1| QAT5CH2| QAT5CH3| QAT5CH4| QAT5CH5| QAT5CH6| QAT5CH7| QAT5CH8| QAT6CH1| QAT6CH2| QAT6CH3| QAT6CH4| QAT6CH5| QAT6CH6| QAT6CH7| QAT6CH8| QAT7CH1| QAT7CH2| QAT7CH3| QAT7CH4| QAT7CH5| QAT7CH6| QAT7CH7| QAT7CH8| QAT8CH1| QAT8CH2| QAT8CH3| QAT8CH4| QAT8CH5| QAT8CH6| QAT8CH7| QAT8CH8| FE1| FE2| FE3| FE4| CFE1| CFE2| CFE3| CFE4 NONE No frontend is mapped. IFONly Selects the IF interface without known frontend. TRX1|TRX2|TRX3|TRX4 Selects the TRX-type frontend and maps it to the respective radar channel. QAT1CH1|QAT1CH2|QAT1CH3|QAT1CH4|QAT1CH5|QAT1CH6|QAT1CH7|QAT1CH8|QAT2CH1|QAT2CH2|QAT2CH3|QAT2CH4|QAT2CH5|QAT2CH6|QAT2CH7|QAT2CH8|QAT3CH1|QAT3CH2|QAT3CH3|QAT3CH4|QAT3CH5|QAT3CH6|QAT3CH7|QAT3CH8|QAT4CH1|QAT4CH2|QAT4CH3|QAT4CH4|QAT4CH5|QAT4CH6|QAT4CH7|QAT4CH8|QAT5CH1|QAT5CH2|QAT5CH3|QAT5CH4|QAT5CH5|QAT5CH6|QAT5CH7|QAT5CH8|QAT6CH1|QAT6CH2|QAT6CH3|QAT6CH4|QAT6CH5|QAT6CH6|QAT6CH7|QAT6CH8|QAT7CH1|QAT7CH2|QAT7CH3|QAT7CH4|QAT7CH5|QAT7CH6|QAT7CH7|QAT7CH8|QAT8CH1|QAT8CH2|QAT8CH3|QAT8CH4|QAT8CH5|QAT8CH6|QAT8CH7|QAT8CH8 Selects the QAT-type frontend and maps it to the respective radar channel. FE1|FE2|FE3|FE4 Selects the FE-type frontend and maps it to the respective radar channel. CFE1|CFE2|CFE3|CFE4 Selects the custom frontend and maps it to the respective radar channel."""
		mappingChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(mappingChannel, repcap.MappingChannel)
		subchannel_cmd_val = self._cmd_group.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:MAPPing{mappingChannel_cmd_val}:SUBChannel{subchannel_cmd_val}:FE?')
		return Conversions.str_to_scalar_enum(response, enums.AregChanMappingGui)
