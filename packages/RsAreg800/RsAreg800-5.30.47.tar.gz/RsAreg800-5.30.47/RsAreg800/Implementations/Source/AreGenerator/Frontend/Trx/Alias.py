from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AliasCls:
	"""Alias commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("alias", core, parent)

	def set(self, areg_fe_alias: str, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ALIas \n
		Snippet: driver.source.areGenerator.frontend.trx.alias.set(areg_fe_alias = 'abc', trxFrontent = repcap.TrxFrontent.Default) \n
		Sets the alias of the frontend. \n
			:param areg_fe_alias: string
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.value_to_quoted_str(areg_fe_alias)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ALIas {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ALIas \n
		Snippet: value: str = driver.source.areGenerator.frontend.trx.alias.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Sets the alias of the frontend. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fe_alias: string"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ALIas?')
		return trim_str_response(response)
