from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def set(self, areg_fe_trx_an_file: str, trxFrontent=repcap.TrxFrontent.Default, rxIndex=repcap.RxIndex.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:RX<ST>:FILE \n
		Snippet: driver.source.areGenerator.frontend.trx.antenna.custom.rx.file.set(areg_fe_trx_an_file = 'abc', trxFrontent = repcap.TrxFrontent.Default, rxIndex = repcap.RxIndex.Default) \n
		No command help available \n
			:param areg_fe_trx_an_file: No help available
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
		"""
		param = Conversions.value_to_quoted_str(areg_fe_trx_an_file)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:RX{rxIndex_cmd_val}:FILE {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default, rxIndex=repcap.RxIndex.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:RX<ST>:FILE \n
		Snippet: value: str = driver.source.areGenerator.frontend.trx.antenna.custom.rx.file.get(trxFrontent = repcap.TrxFrontent.Default, rxIndex = repcap.RxIndex.Default) \n
		No command help available \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:param rxIndex: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rx')
			:return: areg_fe_trx_an_file: No help available"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		rxIndex_cmd_val = self._cmd_group.get_repcap_cmd_value(rxIndex, repcap.RxIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:RX{rxIndex_cmd_val}:FILE?')
		return trim_str_response(response)
