from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwCls:
	"""Bw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bw", core, parent)

	def set(self, areg_fe_bw: float, qatFrontent=repcap.QatFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:BW \n
		Snippet: driver.source.areGenerator.frontend.qat.bw.set(areg_fe_bw = 1.0, qatFrontent = repcap.QatFrontent.Default) \n
		Displays the frequency bandwidth of the output signal of the connected frontend. \n
			:param areg_fe_bw: float Range: 0 to 10E9
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_bw)
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:BW {param}')

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:BW \n
		Snippet: value: float = driver.source.areGenerator.frontend.qat.bw.get(qatFrontent = repcap.QatFrontent.Default) \n
		Displays the frequency bandwidth of the output signal of the connected frontend. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_bw: float Range: 0 to 10E9"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:BW?')
		return Conversions.str_to_float(response)
