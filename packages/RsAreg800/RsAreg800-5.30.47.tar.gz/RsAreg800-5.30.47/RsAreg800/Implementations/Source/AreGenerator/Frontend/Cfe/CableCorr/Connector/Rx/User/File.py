from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def set(self, areg_cable_cor_fil: str, channel=repcap.Channel.Default, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:CABLecorr:CONNector<DI>:RX<ST>:USER:FILE \n
		Snippet: driver.source.areGenerator.frontend.cfe.cableCorr.connector.rx.user.file.set(areg_cable_cor_fil = 'abc', channel = repcap.Channel.Default, connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P. Loads
		a cable correction data file with file extension *.s2p from the default or the specified directory. \n
			:param areg_cable_cor_fil: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
		"""
		param = Conversions.value_to_quoted_str(areg_cable_cor_fil)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:USER:FILE {param}')

	def get(self, channel=repcap.Channel.Default, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:CABLecorr:CONNector<DI>:RX<ST>:USER:FILE \n
		Snippet: value: str = driver.source.areGenerator.frontend.cfe.cableCorr.connector.rx.user.file.get(channel = repcap.Channel.Default, connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P. Loads
		a cable correction data file with file extension *.s2p from the default or the specified directory. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: areg_cable_cor_fil: string"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:USER:FILE?')
		return trim_str_response(response)
