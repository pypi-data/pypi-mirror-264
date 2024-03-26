from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AtsCls:
	"""Ats commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ats", core, parent)

	def set(self, areg_fe_ats: float, qatFrontent=repcap.QatFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:ATS \n
		Snippet: driver.source.areGenerator.frontend.qat.ats.set(areg_fe_ats = 1.0, qatFrontent = repcap.QatFrontent.Default) \n
		Sets the angle between frontend and radar sensor. Reference point for the definition of the angle is the center of the
		frontend. The angle describes the deviation of the position of the frontend from the 0DEG center position of the field of
		view of the radar.
			INTRO_CMD_HELP: We recommend that you zero in regular intervals (at least once a day) , if: \n
			- Positive angle frontend to sensor: counter clockwise deviation of frontend position to center position.
			- Negative angle frontend to sensor: clockwise deviation of frontend position to center position. \n
			:param areg_fe_ats: float Range: -90 to 90
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
		"""
		param = Conversions.decimal_value_to_str(areg_fe_ats)
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:ATS {param}')

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:ATS \n
		Snippet: value: float = driver.source.areGenerator.frontend.qat.ats.get(qatFrontent = repcap.QatFrontent.Default) \n
		Sets the angle between frontend and radar sensor. Reference point for the definition of the angle is the center of the
		frontend. The angle describes the deviation of the position of the frontend from the 0DEG center position of the field of
		view of the radar.
			INTRO_CMD_HELP: We recommend that you zero in regular intervals (at least once a day) , if: \n
			- Positive angle frontend to sensor: counter clockwise deviation of frontend position to center position.
			- Negative angle frontend to sensor: clockwise deviation of frontend position to center position. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_ats: float Range: -90 to 90"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:ATS?')
		return Conversions.str_to_float(response)
