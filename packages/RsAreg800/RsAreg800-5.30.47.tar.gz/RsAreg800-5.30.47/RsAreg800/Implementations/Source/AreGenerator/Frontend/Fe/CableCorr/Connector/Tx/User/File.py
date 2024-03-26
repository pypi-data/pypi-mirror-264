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

	def set(self, areg_cable_cor_fil: str, channel=repcap.Channel.Default, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:CABLecorr:CONNector<DI>:TX<ST0>:USER:FILE \n
		Snippet: driver.source.areGenerator.frontend.fe.cableCorr.connector.tx.user.file.set(areg_cable_cor_fil = 'abc', channel = repcap.Channel.Default, connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P. Loads
		a cable correction data file with file extension *.s2p from the default or the specified directory. \n
			:param areg_cable_cor_fil: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
		"""
		param = Conversions.value_to_quoted_str(areg_cable_cor_fil)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:USER:FILE {param}')

	def get(self, channel=repcap.Channel.Default, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:CABLecorr:CONNector<DI>:TX<ST0>:USER:FILE \n
		Snippet: value: str = driver.source.areGenerator.frontend.fe.cableCorr.connector.tx.user.file.get(channel = repcap.Channel.Default, connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P. Loads
		a cable correction data file with file extension *.s2p from the default or the specified directory. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
			:return: areg_cable_cor_fil: string"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:USER:FILE?')
		return trim_str_response(response)
