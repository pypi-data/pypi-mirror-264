from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, areg_fe_ota_offset: int, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:OTA:OFFSet \n
		Snippet: driver.source.areGenerator.frontend.trx.ota.offset.set(areg_fe_ota_offset = 1, trxFrontent = repcap.TrxFrontent.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param areg_fe_ota_offset: integer Range: 0.01 to 30
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_ota_offset)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:OTA:OFFSet {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:OTA:OFFSet \n
		Snippet: value: int = driver.source.areGenerator.frontend.trx.ota.offset.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fe_ota_offset: integer Range: 0.01 to 30"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:OTA:OFFSet?')
		return Conversions.str_to_int(response)
