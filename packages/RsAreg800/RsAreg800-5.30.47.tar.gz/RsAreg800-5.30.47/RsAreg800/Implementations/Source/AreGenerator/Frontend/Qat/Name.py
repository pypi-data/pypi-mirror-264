from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:NAME \n
		Snippet: value: str = driver.source.areGenerator.frontend.qat.name.get(qatFrontent = repcap.QatFrontent.Default) \n
		Queries the name of the connected frontend. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_name: string"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:NAME?')
		return trim_str_response(response)
