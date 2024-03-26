from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IdCls:
	"""Id commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("id", core, parent)

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:ID \n
		Snippet: value: int = driver.source.areGenerator.frontend.qat.id.get(qatFrontent = repcap.QatFrontent.Default) \n
		No command help available \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_id: No help available"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:ID?')
		return Conversions.str_to_int(response)
