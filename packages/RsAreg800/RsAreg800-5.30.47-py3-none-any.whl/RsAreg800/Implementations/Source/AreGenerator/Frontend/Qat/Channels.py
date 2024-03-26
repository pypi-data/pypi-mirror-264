from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChannelsCls:
	"""Channels commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("channels", core, parent)

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:CHANnels \n
		Snippet: value: int = driver.source.areGenerator.frontend.qat.channels.get(qatFrontent = repcap.QatFrontent.Default) \n
		Queries the number of channels set at the connected QAT-type frontend. The number of channels depends on the 'QAT Channel
		Mode'. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_feq_at_channel: integer Range: 0 to 8"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:CHANnels?')
		return Conversions.str_to_int(response)
