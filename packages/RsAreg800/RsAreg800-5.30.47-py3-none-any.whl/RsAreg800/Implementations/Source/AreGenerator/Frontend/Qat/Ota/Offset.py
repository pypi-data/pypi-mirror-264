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

	def set(self, areg_fe_ota_offset: int, qatFrontent=repcap.QatFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:OTA:OFFSet \n
		Snippet: driver.source.areGenerator.frontend.qat.ota.offset.set(areg_fe_ota_offset = 1, qatFrontent = repcap.QatFrontent.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param areg_fe_ota_offset: integer Range: 0.01 to 30
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_ota_offset)
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:OTA:OFFSet {param}')

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:OTA:OFFSet \n
		Snippet: value: int = driver.source.areGenerator.frontend.qat.ota.offset.get(qatFrontent = repcap.QatFrontent.Default) \n
		Specifies the length of the gap between frontend and target. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_ota_offset: integer Range: 0.01 to 30"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:OTA:OFFSet?')
		return Conversions.str_to_int(response)
