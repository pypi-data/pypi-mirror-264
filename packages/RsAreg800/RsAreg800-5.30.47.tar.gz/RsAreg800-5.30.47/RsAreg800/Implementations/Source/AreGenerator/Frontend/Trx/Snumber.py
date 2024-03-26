from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SnumberCls:
	"""Snumber commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("snumber", core, parent)

	def set(self, areg_fe_ser_number: str, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:SNUMber \n
		Snippet: driver.source.areGenerator.frontend.trx.snumber.set(areg_fe_ser_number = 'abc', trxFrontent = repcap.TrxFrontent.Default) \n
		Queries the 6-digit serial number of the connected frontend. \n
			:param areg_fe_ser_number: string
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.value_to_quoted_str(areg_fe_ser_number)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:SNUMber {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:SNUMber \n
		Snippet: value: str = driver.source.areGenerator.frontend.trx.snumber.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Queries the 6-digit serial number of the connected frontend. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fe_ser_number: string"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:SNUMber?')
		return trim_str_response(response)
