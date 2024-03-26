from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxCls:
	"""Rx commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rx", core, parent)

	def set(self, areg_fe_trx_an_rx: float, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:GAIN:RX \n
		Snippet: driver.source.areGenerator.frontend.trx.antenna.gain.rx.set(areg_fe_trx_an_rx = 1.0, trxFrontent = repcap.TrxFrontent.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>:ANTenna:CUSTom[:MODE] NONe. Displays the antenna gain of the
		receiving antenna (RX) that is mounted on the R&S AREG800A. \n
			:param areg_fe_trx_an_rx: float Range: 0 to 30
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_trx_an_rx)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:GAIN:RX {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:GAIN:RX \n
		Snippet: value: float = driver.source.areGenerator.frontend.trx.antenna.gain.rx.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>:ANTenna:CUSTom[:MODE] NONe. Displays the antenna gain of the
		receiving antenna (RX) that is mounted on the R&S AREG800A. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fe_trx_an_rx: float Range: 0 to 30"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:GAIN:RX?')
		return Conversions.str_to_float(response)
