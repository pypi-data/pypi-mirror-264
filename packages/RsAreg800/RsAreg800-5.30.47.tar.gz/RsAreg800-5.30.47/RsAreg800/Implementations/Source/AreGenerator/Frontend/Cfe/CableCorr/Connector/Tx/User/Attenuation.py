from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AttenuationCls:
	"""Attenuation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuation", core, parent)

	def set(self, areg_cable_corr_at: float, channel=repcap.Channel.Default, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:CABLecorr:CONNector<DI>:TX<ST0>:USER:ATTenuation \n
		Snippet: driver.source.areGenerator.frontend.cfe.cableCorr.connector.tx.user.attenuation.set(areg_cable_corr_at = 1.0, channel = repcap.Channel.Default, connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE USER or
		[:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P.
		Sets a user-defined attenuation value. \n
			:param areg_cable_corr_at: float Range: -50 to 50
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
		"""
		param = Conversions.decimal_value_to_str(areg_cable_corr_at)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:USER:ATTenuation {param}')

	def get(self, channel=repcap.Channel.Default, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:CABLecorr:CONNector<DI>:TX<ST0>:USER:ATTenuation \n
		Snippet: value: float = driver.source.areGenerator.frontend.cfe.cableCorr.connector.tx.user.attenuation.get(channel = repcap.Channel.Default, connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE USER or
		[:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P.
		Sets a user-defined attenuation value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
			:return: areg_cable_corr_at: float Range: -50 to 50"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:USER:ATTenuation?')
		return Conversions.str_to_float(response)
