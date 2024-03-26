from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def set(self, areg_cable_cor_del: float, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:CABLecorr:CONNector<DI>:TX<ST0>:USER:DELay \n
		Snippet: driver.source.areGenerator.swunit.cableCorr.connector.tx.user.delay.set(areg_cable_cor_del = 1.0, connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:SWUNit:CABLecorr:CONNector<di>:RX|TX:MODE USER. Sets a user-defined delay value. \n
			:param areg_cable_cor_del: float Range: 0 to 50
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
		"""
		param = Conversions.decimal_value_to_str(areg_cable_cor_del)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SWUNit:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:USER:DELay {param}')

	def get(self, connector=repcap.Connector.Default, txIndexNull=repcap.TxIndexNull.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:CABLecorr:CONNector<DI>:TX<ST0>:USER:DELay \n
		Snippet: value: float = driver.source.areGenerator.swunit.cableCorr.connector.tx.user.delay.get(connector = repcap.Connector.Default, txIndexNull = repcap.TxIndexNull.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:SWUNit:CABLecorr:CONNector<di>:RX|TX:MODE USER. Sets a user-defined delay value. \n
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param txIndexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
			:return: areg_cable_cor_del: float Range: 0 to 50"""
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		txIndexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(txIndexNull, repcap.TxIndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SWUNit:CABLecorr:CONNector{connector_cmd_val}:TX{txIndexNull_cmd_val}:USER:DELay?')
		return Conversions.str_to_float(response)
