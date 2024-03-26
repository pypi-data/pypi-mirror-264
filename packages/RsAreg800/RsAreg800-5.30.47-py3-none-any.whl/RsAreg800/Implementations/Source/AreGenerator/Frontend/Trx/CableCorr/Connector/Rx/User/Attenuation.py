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

	def set(self, areg_cable_corr_at: float, trxFrontent=repcap.TrxFrontent.Default, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:CABLecorr:CONNector<DI>:RX<ST>:USER:ATTenuation \n
		Snippet: driver.source.areGenerator.frontend.trx.cableCorr.connector.rx.user.attenuation.set(areg_cable_corr_at = 1.0, trxFrontent = repcap.TrxFrontent.Default, connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE USER or
		[:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P.
		Sets a user-defined attenuation value. \n
			:param areg_cable_corr_at: float Range: -50 to 50
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
		"""
		param = Conversions.decimal_value_to_str(areg_cable_corr_at)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:USER:ATTenuation {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:CABLecorr:CONNector<DI>:RX<ST>:USER:ATTenuation \n
		Snippet: value: float = driver.source.areGenerator.frontend.trx.cableCorr.connector.rx.user.attenuation.get(trxFrontent = repcap.TrxFrontent.Default, connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE USER or
		[:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>|QAT<ch>|FE<ch>|CFE<ch>:CABLecorr:CONNector<di>:RX|TX:MODE S2P.
		Sets a user-defined attenuation value. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: areg_cable_corr_at: float Range: -50 to 50"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:USER:ATTenuation?')
		return Conversions.str_to_float(response)
