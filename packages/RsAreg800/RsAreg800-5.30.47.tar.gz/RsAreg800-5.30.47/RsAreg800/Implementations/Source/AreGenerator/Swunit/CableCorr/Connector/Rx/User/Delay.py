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

	def set(self, areg_cable_cor_del: float, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:CABLecorr:CONNector<DI>:RX<ST>:USER:DELay \n
		Snippet: driver.source.areGenerator.swunit.cableCorr.connector.rx.user.delay.set(areg_cable_cor_del = 1.0, connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:SWUNit:CABLecorr:CONNector<di>:RX|TX:MODE USER. Sets a user-defined delay value. \n
			:param areg_cable_cor_del: float Range: 0 to 50
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
		"""
		param = Conversions.decimal_value_to_str(areg_cable_cor_del)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SWUNit:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:USER:DELay {param}')

	def get(self, connector=repcap.Connector.Default, rxIndex=repcap.RxIndex.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:CABLecorr:CONNector<DI>:RX<ST>:USER:DELay \n
		Snippet: value: float = driver.source.areGenerator.swunit.cableCorr.connector.rx.user.delay.get(connector = repcap.Connector.Default, rxIndex = repcap.RxIndex.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:SWUNit:CABLecorr:CONNector<di>:RX|TX:MODE USER. Sets a user-defined delay value. \n
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: areg_cable_cor_del: float Range: 0 to 50"""
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:SWUNit:CABLecorr:CONNector{connector_cmd_val}:RX{rxIndex_cmd_val}:USER:DELay?')
		return Conversions.str_to_float(response)
